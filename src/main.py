"""
Main entry point for the Meteoro Station.
Integrates acquisition, storage, web server, and watchdog functionalities,
utilizing dynamic hardware detection with fallback to mocks.
"""

import asyncio

try:
    from machine import WDT
except ImportError:
    WDT = None

from src.core.acquisition import AcquisitionManager
from src.core.csv_storage import CSVManager
from src.core.storage import CircularBuffer
from src.sensors.factory import load_bme_sensor, load_gas_sensor
from src.web.server import init_app


async def watchdog_task(wdt, interval: int = 5):
    """
    Periodically feeds the watchdog timer to prevent system resets.

    Args:
        wdt: Watchdog timer instance or None.
        interval (int): Time in seconds between feed cycles.
    """
    if wdt is None:
        return

    while True:
        wdt.feed()
        await asyncio.sleep(interval)


async def main():
    """
    Initializes system components (buffer, storage, sensors via factory, and web app)
    and runs the concurrent system tasks.
    """
    buffer = CircularBuffer(capacity=144)
    csv_manager = CSVManager("history.csv")

    bme_sensor = load_bme_sensor()
    gas_sensor = load_gas_sensor()

    acquisition = AcquisitionManager(
        bme_sensor, gas_sensor, buffer, csv_manager, interval_sec=10
    )
    app = init_app(buffer)

    wdt = WDT(timeout=30000) if WDT else None

    tasks = [
        asyncio.create_task(acquisition.run()),
        asyncio.create_task(watchdog_task(wdt)),
        asyncio.create_task(app.start_server(port=80, debug=False)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Sistema parado manualmente.")
