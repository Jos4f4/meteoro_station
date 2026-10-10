"""
Sensor Factory module for dynamic hardware detection and fallback to Mocks.
Provides adapters for physical sensors (BME280, DHT11, MQ-2, DS3231)
ensuring interface consistency with mock counterparts.
"""

import time

import bme280
import dht
from machine import ADC, I2C, Pin

from src.sensors.mock_gas_sensor import MockGasSensor
from src.sensors.mock_sensors import MockBME280


class RealBME280Adapter:
    """
    Adapter for the physical BME280 barometric pressure,
    temperature, and humidity sensor over I2C.
    """

    def __init__(self, i2c):
        """
        Initializes the BME280 physical driver wrapper.

        Args:
            i2c: Initialized I2C bus instance.
        """
        self.sensor = bme280.BME280(i2c=i2c)

    def read(self) -> dict:
        """
        Reads environmental parameters from the physical BME280 sensor.

        Returns:
            dict: Temperature, humidity, and pressure values.
        """
        t, p, h = self.sensor.read()
        return {
            "temperature": float(t.replace("C", "")),
            "humidity": float(h.replace("%", "")),
            "pressure": float(p.replace("hPa", "")),
        }


class RealDHT11Adapter:
    """
    Adapter for the physical DHT11 temperature and humidity sensor.
    """

    def __init__(self, pin_number: int):
        """
        Initializes the DHT11 driver on a specific GPIO pin.

        Args:
            pin_number (int): GPIO pin connected to the DHT11 data line.
        """
        self.sensor = dht.DHT11(Pin(pin_number))

    def read(self) -> dict:
        """
        Triggers a measurement and retrieves data from the DHT11 sensor.

        Returns:
            dict: Temperature and humidity readings, or None on failure.
        """
        try:
            self.sensor.measure()
            return {
                "temperature": float(self.sensor.temperature()),
                "humidity": float(self.sensor.humidity()),
                "pressure": None,
            }
        
        except Exception:
            return {"temperature": None, "humidity": None, "pressure": None}


class RealMQ2Adapter:
    """
    Adapter for the physical MQ-2 gas and smoke sensor connected via ADC.
    """

    def __init__(self, pin_number: int):
        """
        Initializes the ADC pin configuration for the MQ-2 sensor.

        Args:
            pin_number (int): ADC-capable GPIO pin.
        """
        self.adc = ADC(Pin(pin_number))
        self.adc.atten(ADC.ATTN_11DB)  # Full range 0-3.3V

    def read(self) -> dict:
        """
        Reads the analog gas concentration level.

        Returns:
            dict: Air quality index and operational state.
        """
        val = self.adc.read()
        return {"air_quality_index": float(val), "state": "valid"}


class RealDS3231Adapter:
    """
    Adapter for the DS3231 Real-Time Clock (RTC) module over I2C.
    """

    def __init__(self, i2c):
        """
        Initializes the DS3231 RTC wrapper.

        Args:
            i2c: Initialized I2C bus instance.
        """
        self.i2c = i2c
        self.addr = 0x68

    def get_time(self) -> tuple:
        """
        Retrieves the current date and time from the RTC module.

        Returns:
            tuple: Raw byte data or system timestamp as fallback.
        """
        try:
            data = self.i2c.readfrom_mem(self.addr, 0, 7)
            return data
        
        except Exception:
            return time.time()


def load_bme_sensor():
    """
    Factory function to detect and load the BME280 hardware via I2C,
    falling back to MockBME280 if the sensor is absent.

    Returns:
        RealBME280Adapter or MockBME280: The active sensor instance.
    """
    try:
        
        i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        devices = i2c.scan()
        if 0x76 in devices or 0x77 in devices:
            return RealBME280Adapter(i2c)

    except Exception:
        pass

    return MockBME280()


def load_gas_sensor():
    """
    Factory function to initialize the MQ-2 gas sensor hardware,
    falling back to MockGasSensor if unavailable.

    Returns:
        RealMQ2Adapter or MockGasSensor: The active gas sensor instance.
    """
    try:
        return RealMQ2Adapter(34)

    except Exception:
        pass

    return MockGasSensor(heating_time_seconds=10)
