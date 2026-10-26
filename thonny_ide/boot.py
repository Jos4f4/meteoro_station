"""
Boot file for the Meteorological Station.
"""
import network
import time

sta = network.WLAN(network.STA_IF)
sta.active(False)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="Meteoro_Station")

time.sleep(2)
print("Station Wi-Fi network active. IP:", ap.ifconfig()[0])