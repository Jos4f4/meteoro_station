"""
Main entry point for the Meteoro Station.
Integrates acquisition, storage, web server, and watchdog functionalities.
"""
import asyncio

try:

    from machine import WDT

except ImportError:
    WDT = None

from src.core.acquisition import AcquisitionManager
from src.core.storage import CircularBuffer
from src.sensors.mock_gas_sensor import MockGasSensor
from src.sensors.mock_sensors import MockBME280
from src.web.server import init_app


async def watchdog_task(wdt, interval: int = 5):
    """
    Periodically feeds the watchdog timer to prevent system resets.
    """
    if wdt is None:
        return
        
    while True:
        wdt.feed()
        await asyncio.sleep(interval)


async def main():
    """
    Initializes components and runs the concurrent system tasks.
    """
    buffer = CircularBuffer(capacity=144)
    
    bme_sensor = MockBME280()
    gas_sensor = MockGasSensor(heating_time_seconds=10)

    acquisition = AcquisitionManager(bme_sensor, gas_sensor, buffer, interval_sec=10)
    app = init_app(buffer)
    
    # Watchdog configurado para 30000ms (30 segundos) conforme RF18
    wdt = WDT(timeout=30000) if WDT else None
    
    tasks = [
        asyncio.create_task(acquisition.run()),
        asyncio.create_task(watchdog_task(wdt)),
        asyncio.create_task(app.start_server(port=80, debug=False))
    ]
    
    await asyncio.gather(*tasks)


if __name__ == '__main__':

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("Sistema parado manualmente.")
