"""
Unit tests for the boot network initialization.
"""

import sys
from unittest.mock import MagicMock

mock_network = MagicMock()
sys.modules["network"] = mock_network

from src.boot import setup_ap


def test_setup_ap_activates_wlan():
    """
    Ensures the AP mode is correctly configured and activated using the network module.
    """
    mock_network.reset_mock()

    mock_wlan = MagicMock()
    mock_network.WLAN.return_value = mock_wlan
    mock_network.AP_IF = 1
    mock_wlan.active.return_value = True

    result = setup_ap(ssid="Meteoro_Test", password="password123")

    mock_network.WLAN.assert_called_once_with(1)
    mock_wlan.active.assert_any_call(True)
    mock_wlan.config.assert_called_once_with(
        essid="Meteoro_Test", password="password123"
    )

    assert result is True
