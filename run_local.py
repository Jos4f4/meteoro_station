import sys
from unittest.mock import MagicMock

sys.modules["machine"] = MagicMock()
sys.modules["bme280"] = MagicMock()
sys.modules["dht"] = MagicMock()

import asyncio

from src.main import main

if __name__ == "__main__":
    print("A iniciar Estação Meteorológica (Simulação Local)...")
    print("Acesse http://localhost no seu navegador.")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor parado manualmente.")
