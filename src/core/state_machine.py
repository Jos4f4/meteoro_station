"""
State machine module for managing sensor states and reading classifications.
"""


class SensorState:
    """
    Constants representing the operational state of a physical sensor.
    """

    VALID = "valid"
    HEATING = "heating"
    OFFLINE = "offline"
    OUT_OF_RANGE = "out_of_range"


class ReadingCategory:
    """
    Constants representing the environmental classification of a reading.
    """

    NORMAL = "normal"
    ATTENTION = "attention"
    CRITICAL = "critical"


class SensorEvaluator:
    """
    Evaluates sensor readings and determines their operational state
    and environmental classification based on configured thresholds.
    """

    def __init__(self, limits: dict):
        """
        Initializes the evaluator with defined environmental limits.

        Args:
            limits (dict): Configuration dictionary containing thresholds.
        """

        self.limits = limits

    def evaluate_reading(self, value: float, sensor_type: str) -> str:
        """
        Classifies a reading into normal, attention, or critical categories.

        Args:
            value (float): The current sensor reading value.
            sensor_type (str): The type of the sensor (e.g., 'temperature').

        Returns:
            str: The classification category (normal, attention, or critical).
        """
        
        if sensor_type not in self.limits:
            return ReadingCategory.NORMAL

        sensor_limits = self.limits[sensor_type]
        
        if value >= sensor_limits.get("critical", float('inf')):
            return ReadingCategory.CRITICAL
        
        if value >= sensor_limits.get("attention", float('inf')):
            return ReadingCategory.ATTENTION

        return ReadingCategory.NORMAL
    