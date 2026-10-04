"""
CSV storage module for persistent historical data on LittleFS.
"""

import os


class CSVManager:
    """
    Manages the appending of sensor readings to a persistent CSV file.
    """

    def __init__(self, filepath: str = "history.csv"):
        """
        Initializes the manager and creates the CSV file with headers if it doesn't exist.
        """
        self.filepath = filepath
        self._init_file()

    def _init_file(self) -> None:
        """
        Checks if the file exists; if not, writes the CSV header.
        """
        try:
            os.stat(self.filepath)
        except OSError:
            # File does not exist, create it and write the header
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(
                    "timestamp,temperature,humidity,pressure,air_quality_index,gas_state\n"
                )

    def append_reading(self, reading: dict) -> None:
        """
        Appends a single reading dictionary as a CSV row.

        Args:
            reading (dict): The environmental data to store.
        """
        row = (
            f"{reading.get('timestamp', '')},"
            f"{reading.get('temperature', '')},"
            f"{reading.get('humidity', '')},"
            f"{reading.get('pressure', '')},"
            f"{reading.get('air_quality_index', '')},"
            f"{reading.get('gas_state', '')}\n"
        )
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(row)
