import sys
from unittest.mock import MagicMock

sys.modules["machine"] = MagicMock()
sys.modules["bme280"] = MagicMock()
sys.modules["dht"] = MagicMock()