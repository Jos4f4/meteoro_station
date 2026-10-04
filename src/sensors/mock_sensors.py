"""
Mock sensors for local development and testing without physical hardware.
"""

import random
import time


class MockBME280:
    """
    Simulates the BME280 sensor providing temperature, humidity, and pressure.
    """

    def __init__(self):
        """
        Initializes the mock sensor with default simulated states.
        """
        self.state = "valid"
        self.last_read_time = time.time()

    def read(self) -> dict:
        """
        Simulates reading data from the environment.

        Returns:
            dict: A dictionary containing temperature, humidity, and pressure.
        """
        return {
            "temperature": round(random.uniform(25.0, 38.0), 1),
            "humidity": round(random.uniform(60.0, 95.0), 1),
            "pressure": round(random.uniform(1000.0, 1020.0), 1),
        }
