"""
Asynchronous acquisition task manager for polling sensors.
"""

import asyncio
import time

from src.core.csv_storage import CSVManager
from src.core.storage import CircularBuffer


class AcquisitionManager:
    """
    Manages periodic sensor readings and stores them in the circular buffer and CSV.
    """

    def __init__(
        self,
        bme_sensor,
        gas_sensor,
        buffer: CircularBuffer,
        csv_manager: CSVManager = None,
        interval_sec: int = 10,
    ):
        self.bme_sensor = bme_sensor
        self.gas_sensor = gas_sensor
        self.buffer = buffer
        self.csv_manager = csv_manager
        self.interval = interval_sec
        self.is_running = False

    async def run(self) -> None:
        """
        Starts the infinite loop to acquire data from sensors asynchronously.
        """
        self.is_running = True
        while self.is_running:
            timestamp = time.time()

            # Read sensors
            bme_data = self.bme_sensor.read()
            gas_data = self.gas_sensor.read()

            # Compile the consolidated reading
            compiled_reading = {
                "timestamp": timestamp,
                "temperature": bme_data.get("temperature"),
                "humidity": bme_data.get("humidity"),
                "pressure": bme_data.get("pressure"),
                "air_quality_index": gas_data.get("air_quality_index"),
                "bme_state": "valid",
                "gas_state": gas_data.get("state"),
            }

            self.buffer.add_reading(compiled_reading)

            if self.csv_manager:
                self.csv_manager.append_reading(compiled_reading)

            await asyncio.sleep(self.interval)

    def stop(self) -> None:
        self.is_running = False