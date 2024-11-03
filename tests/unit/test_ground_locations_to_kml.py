"""
Test Process.
"""

import pathlib

import pytest

from modules.kml import ground_locations_to_kml
from modules.kml import named_location_global


PARENT_DIRECTORY = pathlib.Path("tests", "unit", "kml_documents")
EXPECTED_KML_DOCUMENT_PATH = pathlib.Path(PARENT_DIRECTORY, "expected_document.kml")


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def locations() -> "list[named_location_global.NamedLocationGlobal]":  # type: ignore
    """
    List of LocationGround.
    """
    result, location_san_francisco = named_location_global.NamedLocationGlobal.create(
        "San Francisco", 37.7749, -122.4194
    )
    assert result
    assert location_san_francisco is not None

    result, location_los_angeles = named_location_global.NamedLocationGlobal.create(
        "Los Angeles", 34.0522, -118.2437
    )
    assert result
    assert location_los_angeles is not None

    result, location_new_york_city = named_location_global.NamedLocationGlobal.create(
        "New York City", 40.7128, -74.0060
    )
    assert result
    assert location_new_york_city is not None

    yield [
        location_san_francisco,
        location_los_angeles,
        location_new_york_city,
    ]


def test_locations_to_kml_with_save_path(
    locations: "list[named_location_global.NamedLocationGlobal]", tmp_path: pathlib.Path
) -> None:
    """
    Basic test case to save KML to the correct path when provided.
    """
    actual_kml_document_name = "actual_kml_document"

    # Build a temporary directory using tmp_path so
    # the KML files are cleaned after the tests are run
    tmp_path.mkdir(parents=True, exist_ok=True)

    result, actual_kml_file_path = ground_locations_to_kml.ground_locations_to_kml(
        locations,
        actual_kml_document_name,
        tmp_path,
    )

    # Assert success
    assert result
    assert actual_kml_file_path is not None

    # Assert that the KML file has been generated properly in the provided path
    assert actual_kml_file_path.exists()
    assert actual_kml_file_path.suffix == ".kml"

    # Compare the contents of the generated KML file with the static KML file
    assert actual_kml_file_path.read_text(encoding="utf-8") == EXPECTED_KML_DOCUMENT_PATH.read_text(
        encoding="utf-8"
    )