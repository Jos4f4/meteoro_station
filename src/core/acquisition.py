"""
Asynchronous acquisition task manager for polling sensors.
"""

import asyncio
import time

from src.core.storage import CircularBuffer


class AcquisitionManager:
    """
    Manages periodic sensor readings and stores them in the circular buffer.
    """

    def __init__(
        self, bme_sensor, gas_sensor, buffer: CircularBuffer, interval_sec: int = 10
    ):
        """
        Initializes the acquisition manager.

        Args:
            bme_sensor: Instance of the BME280 sensor (or mock).
            gas_sensor: Instance of the Gas sensor (or mock).
            buffer (CircularBuffer): The storage buffer.
            interval_sec (int): Polling interval in seconds.
        """

        self.bme_sensor = bme_sensor
        self.gas_sensor = gas_sensor
        self.buffer = buffer
        self.interval = interval_sec
        self.is_running = False

    async def run(self) -> None:
        """
        Starts the infinite loop to acquire data from sensors asynchronously.
        """

        self.is_running = True
        while self.is_running:
            timestamp = time.time()  # Using standard time, can be ISO 8601 later

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
                "bme_state": "valid",  # Hardcoded for the mock for now
                "gas_state": gas_data.get("state"),
            }

            self.buffer.add_reading(compiled_reading)

            # Non-blocking wait for the next cycle
            await asyncio.sleep(self.interval)

    def stop(self) -> None:
        """
        Stops the acquisition loop.
        """

        self.is_running = False
