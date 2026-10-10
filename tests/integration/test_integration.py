"""
Integration tests for the acquisition pipeline.
Validates the interaction between the sensor factory, RAM storage (buffer),
and persistent physical storage (CSV).
"""

import asyncio

import pytest

from src.core.acquisition import AcquisitionManager
from src.core.csv_storage import CSVManager
from src.core.storage import CircularBuffer
from src.sensors.factory import load_bme_sensor, load_gas_sensor


@pytest.mark.asyncio
async def test_acquisition_flow_with_factory_and_storage(tmp_path):
    """
    Tests the complete data acquisition flow.
    Ensures that data from sensors (or fallback mocks) is correctly collected,
    stored in the RAM circular buffer, and successfully written to a CSV file.

    Args:
        tmp_path: Pytest fixture providing a temporary directory unique to this 
        test invocation.
    """
    csv_file = tmp_path / "test_history.csv"
    csv_manager = CSVManager(str(csv_file))
    buffer = CircularBuffer(capacity=10)
    
    bme = load_bme_sensor()
    gas = load_gas_sensor()
    
    acquisition = AcquisitionManager(bme, gas, buffer, csv_manager, interval_sec=0.1)
    
    task = asyncio.create_task(acquisition.run())
    await asyncio.sleep(0.2)
    acquisition.stop()
    await task
    
    latest = buffer.get_latest()
    assert latest != {}
    assert "temperature" in latest
    
    assert csv_file.exists()
    content = csv_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) >= 2
