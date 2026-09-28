"""
Boot script for ESP32.
Initializes the Wi-Fi Access Point (AP) mode as required by RF14.
"""
try:
    import network

except ImportError:

    network = None


def setup_ap(ssid: str = "Meteoro_Station", password: str = "fametro2026") -> bool:
    """
    Configures the ESP32 as a Wi-Fi Access Point.
    
    Args:
        ssid (str): The network name.
        password (str): The network password (minimum 8 characters).
        
    Returns:
        bool: True if AP is active and configured, False otherwise.
    """
    if network is None:

        print("Módulo 'network' não encontrado. Rodando em modo de simulação.")
        return False

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    
    print(f"Modo AP inicializado: {ssid}")
    print(f"Configuração de rede: {ap.ifconfig()}")
    
    return ap.active()


if __name__ == '__main__':
    setup_ap()
