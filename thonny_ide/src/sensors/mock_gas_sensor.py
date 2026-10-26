"""
Mock gas sensor (e.g., MQ-135) to simulate heating states and relative indices.
"""

import random
import time

from src.core.state_machine import SensorState


class MockGasSensor:
    """
    Simulates a gas sensor that requires an initial heating period before
    providing valid relative index readings.
    """

    def __init__(self, heating_time_seconds: int = 10):
        """
        Initializes the mock gas sensor.

        Args:
            heating_time_seconds (int): Time required for the sensor to heat up.
        """
        self.start_time = time.time()
        self.heating_time = heating_time_seconds

    def get_state(self) -> str:
        """
        Determines the current operational state of the sensor.

        Returns:
            str: The current state (heating or valid).
        """
        if (time.time() - self.start_time) < self.heating_time:
            return SensorState.HEATING

        return SensorState.VALID

    def read(self) -> dict:
        """
        Simulates reading the air quality relative index.

        Returns:
            dict: A dictionary containing the air quality index and sensor state.
        """
        state = self.get_state()
        reading = {"state": state, "air_quality_index": None}

        if state == SensorState.VALID:
            reading["air_quality_index"] = round(random.uniform(50.0, 150.0), 1)

        return reading