"""
Unit tests for core components and factory modules.
Validates the circular buffer, sensor evaluator logic, and hardware factory fallbacks.
"""

from src.core.state_machine import ReadingCategory, SensorEvaluator
from src.core.storage import CircularBuffer
from src.sensors.factory import load_bme_sensor, load_gas_sensor
from src.sensors.mock_gas_sensor import MockGasSensor
from src.sensors.mock_sensors import MockBME280


def test_circular_buffer_capacity():
    """
    Tests if the CircularBuffer correctly maintains its maximum capacity
    by overwriting the oldest readings when full.
    """
    buffer = CircularBuffer(capacity=3)
    for i in range(1, 5):
        buffer.add_reading({"id": i})

    all_items = buffer.get_all()
    assert len(all_items) == 3
    assert all_items[-1]["id"] == 4
    assert all_items[0]["id"] == 2


def test_sensor_evaluator_thresholds():
    """
    Validates the SensorEvaluator logic to ensure readings are correctly
    classified as NORMAL, ATTENTION, or CRITICAL based on defined thresholds.
    """
    limits = {"temperature": {"attention": 30.0, "critical": 35.0}}
    evaluator = SensorEvaluator(limits)

    assert evaluator.evaluate_reading(25.0, "temperature") == ReadingCategory.NORMAL
    assert evaluator.evaluate_reading(32.0, "temperature") == ReadingCategory.ATTENTION
    assert evaluator.evaluate_reading(38.0, "temperature") == ReadingCategory.CRITICAL


def test_factory_fallback_to_mocks(monkeypatch):
    """
    Tests the dynamic sensor factory to ensure it correctly falls back
    to Mock sensors when hardware initialization fails.

    Args:
        monkeypatch: Pytest fixture to mock hardware initialization failures.
    """
    # Força um erro na inicialização do sensor real para simular a ausência de hardware
    def mock_hardware_failure(*args, **kwargs):
        raise RuntimeError("Hardware ADC ausente")

    monkeypatch.setattr(
        "src.sensors.factory.RealMQ2Adapter.__init__", mock_hardware_failure
    )

    bme = load_bme_sensor()
    gas = load_gas_sensor()

    assert isinstance(bme, MockBME280)
    assert isinstance(gas, MockGasSensor)
