"""
Storage module for managing the circular buffer of sensor readings in RAM.
"""


class CircularBuffer:
    """
    A circular buffer that holds a fixed number of the most recent readings.
    When the buffer reaches its maximum capacity, the oldest reading is overwritten.
    """

    def __init__(self, capacity: int = 144):
        """
        Initializes the circular buffer.
        
        Args:
            capacity (int): Maximum number of readings to store. 
            Default 144 (e.g., 24h of 10-minute intervals).
        """

        self.capacity = capacity
        self.buffer = []
        self.index = 0

    def add_reading(self, reading: dict) -> None:
        """
        Adds a new reading to the buffer.
        
        Args:
            reading (dict): The sensor data dictionary to store.
        """

        if len(self.buffer) < self.capacity:
            self.buffer.append(reading)
        else:
            self.buffer[self.index] = reading
            self.index = (self.index + 1) % self.capacity

    def get_latest(self) -> dict:
        """
        Retrieves the most recent reading.
        
        Returns:
            dict: The latest reading, or an empty dictionary if the buffer is empty.
        """

        if not self.buffer:
            return {}
        
        # If buffer is full, the latest item is just before the current index
        latest_index = (self.index - 1) if len(self.buffer) == self.capacity else -1

        return self.buffer[latest_index]

    def get_all(self) -> list:
        """
        Retrieves all readings in chronological order (oldest to newest).
        
        Returns:
            list: A list of reading dictionaries.
        """
        
        if len(self.buffer) < self.capacity:
            return self.buffer
        
        return self.buffer[self.index:] + self.buffer[:self.index]
