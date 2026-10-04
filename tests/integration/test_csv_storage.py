"""
Integration tests for CSV persistent storage.
"""

import os

import pytest

from src.core.csv_storage import CSVManager


@pytest.fixture
def temp_csv_file():
    """
    Provides a temporary filename and cleans it up after the test.
    """
    filename = "test_history.csv"
    yield filename
    # Cleanup after test
    if os.path.exists(filename):
        os.remove(filename)


def test_csv_creates_header_if_missing(temp_csv_file):
    """
    Ensures the header is written when the file is created.
    """
    CSVManager(filepath=temp_csv_file)

    with open(temp_csv_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert "timestamp,temperature,humidity" in lines[0]


def test_csv_appends_data_correctly(temp_csv_file):
    """
    Ensures that readings are appended sequentially.
    """
    manager = CSVManager(filepath=temp_csv_file)

    reading_1 = {
        "timestamp": "2026-09-20T10:00:00Z",
        "temperature": 30.5,
        "humidity": 80.0,
        "pressure": 1010.5,
        "air_quality_index": 100.0,
        "gas_state": "valid",
    }

    reading_2 = {
        "timestamp": "2026-09-20T10:10:00Z",
        "temperature": 31.0,
        "humidity": 78.5,
        "pressure": 1011.0,
        "air_quality_index": 105.0,
        "gas_state": "valid",
    }

    manager.append_reading(reading_1)
    manager.append_reading(reading_2)

    with open(temp_csv_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 3
    assert "30.5,80.0" in lines[1]
    assert "31.0,78.5" in lines[2]
