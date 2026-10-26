"""
Main entry point for the Meteoro Station.
Fully integrated native HTTP server supporting static assets, API, and CSV export.
"""

import gc
import asyncio
import usocket as socket
import json

from src.core.acquisition import AcquisitionManager
from src.core.csv_storage import CSVManager
from src.core.storage import CircularBuffer
from src.sensors.factory import load_bme_sensor, load_gas_sensor

gc.collect()

async def web_server_task(buffer, csv_manager):
    """
    Native lightweight HTTP server loop with comprehensive path routing for assets and API.
    """
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    s.setblocking(False)
    
    print("Native HTTP server with asset and API support active on port 80...")
    
    while True:
        try:
            await asyncio.sleep(0.05)
            
            try:
                conn, client_addr = s.accept()
            except OSError:
                continue 
            
            request = conn.recv(1024).decode('utf-8')
            if not request:
                conn.close()
                continue
            
            first_line = request.split('\r\n')[0]
            parts = first_line.split(' ')
            path = parts[1] if len(parts) > 1 else '/'
            
            content_type = 'text/plain'
            body = ""
            
            # 1. Main Page (HTML)
            if path == '/' or path == '/index.html':
                try:
                    with open('src/web/static/index.html', 'r', encoding='utf-8') as f:
                        body = f.read()
                    content_type = 'text/html'
                except Exception as e:
                    body = f"Error reading index.html: {e}"
            
            # 2. Static Files (app.js, style.css)
            elif path in ['/app.js', '/style.css'] or path.startswith('/static/'):
                filename = path.split('/')[-1]
                ext = filename.split('.')[-1]
                content_types = {
                    'css': 'text/css', 
                    'js': 'application/javascript',
                    'html': 'text/html'
                }
                content_type = content_types.get(ext, 'text/plain')
                try:
                    with open(f'src/web/static/{filename}', 'r', encoding='utf-8') as f:
                        body = f.read()
                except Exception:
                    body = "Static file not found"
            
            # 3. API Endpoint (Feeds sensor blocks)
            elif path == '/api':
                latest_data = buffer.get_latest()
                if not latest_data:
                    latest_data = {
                        "temperature": {"value": 0.0},
                        "humidity": {"value": 0.0},
                        "pressure": {"value": 0.0},
                        "air_quality_index": {"value": 0}
                    }
                body = json.dumps(latest_data)
                content_type = 'application/json'
                
            # 4. CSV History Download Endpoint
            elif path in ['/api/exportar.csv', '/exportar.csv', '/history.csv']:
                try:
                    with open('history.csv', 'r', encoding='utf-8') as f:
                        body = f.read()
                    content_type = 'text/csv'
                except Exception:
                    body = "timestamp,temperature,humidity,pressure,air_quality_index\n"
                    content_type = 'text/csv'
                    
            else:
                body = "404 Not Found"
                content_type = 'text/plain'
            
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Access-Control-Allow-Origin: *\r\n"
                f"Connection: close\r\n\r\n"
                f"{body}"
            )
            
            conn.send(response.encode('utf-8'))
            conn.close()
            
        except Exception as e:
            print("Error in web server:", e)

async def main():
    """
    Initializes components, background data acquisition, and web server.
    """
    buffer = CircularBuffer(capacity=144)
    csv_manager = CSVManager("history.csv")

    bme_sensor = load_bme_sensor()
    gas_sensor = load_gas_sensor()

    acquisition = AcquisitionManager(
        bme_sensor, gas_sensor, buffer, csv_manager, interval_sec=5
    )

    gc.collect()
    await asyncio.sleep(1)

    tasks = [
        asyncio.create_task(acquisition.run()),
        asyncio.create_task(web_server_task(buffer, csv_manager)),
    ]

    await asyncio.gather(*tasks)