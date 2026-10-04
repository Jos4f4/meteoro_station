"""
Unit tests for the asynchronous AcquisitionManager.
"""

import asyncio

import pytest

from src.core.acquisition import AcquisitionManager
from src.core.storage import CircularBuffer
from src.sensors.mock_gas_sensor import MockGasSensor
from src.sensors.mock_sensors import MockBME280


@pytest.mark.asyncio
async def test_acquisition_loop_integrates_data():
    """
    Test if the manager reads from sensors and populates the buffer.
    """
    buffer = CircularBuffer(capacity=5)
    bme = MockBME280()
    gas = MockGasSensor(heating_time_seconds=0)  # No heating time for fast test

    manager = AcquisitionManager(bme, gas, buffer, interval_sec=0.1)

    task = asyncio.create_task(manager.run())

    await asyncio.sleep(0.25)
    manager.stop()
    await task

    readings = buffer.get_all()
    assert len(readings) >= 2

    latest = buffer.get_latest()
    assert "timestamp" in latest
    assert "temperature" in latest
    assert "air_quality_index" in latest
    assert latest["gas_state"] == "valid"
