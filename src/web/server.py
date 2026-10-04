"""
Embedded Web Server module using Microdot for the ESP32.
Serves both the REST API and the static frontend files.
"""

import json
from pathlib import Path

from microdot import Microdot, Response

app = Microdot()
_storage_buffer = None

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


def init_app(buffer_instance):
    """
    Initializes the web application with the shared data buffer.

    Args:
        buffer_instance (CircularBuffer): The RAM storage buffer.

    Returns:
        Microdot: The configured application instance.
    """
    global _storage_buffer
    _storage_buffer = buffer_instance

    return app


@app.route("/api")
async def get_latest_readings(request):
    """
    API endpoint that returns the most recent
    environmental readings in JSON format.
    """
    if not _storage_buffer:
        return Response(
            body=json.dumps({"error": "Buffer not initialized"}),
            status_code=500,
            headers={"Content-Type": "application/json"},
        )

    latest_data = _storage_buffer.get_latest()

    return Response(
        body=json.dumps(latest_data),
        status_code=200,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    )


@app.route("/")
async def serve_index(request):
    """
    Serves the main dashboard HTML file.
    """
    try:
        file_path = STATIC_DIR / "index.html"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return Response(
            body=content, status_code=200, headers={"Content-Type": "text/html"}
        )

    except Exception as e:
        return Response(
            body=f"Error reading index.html: {e} | Path attempted: {file_path}",
            status_code=404,
        )


@app.route("/static/<path:filename>")
async def serve_static(request, filename):
    """
    Serves static CSS and JS files based on the requested filename.
    """
    content_types = {"css": "text/css", "js": "application/javascript"}
    ext = filename.split(".")[-1]
    content_type = content_types.get(ext, "text/plain")

    try:
        file_path = STATIC_DIR / filename

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return Response(
            body=content, status_code=200, headers={"Content-Type": content_type}
        )

    except Exception as e:
        return Response(
            body=f"Error reading {filename}: {e} | Path attempted: {file_path}",
            status_code=404,
        )


@app.route("/api/exportar.csv")
async def export_csv(request):
    """
    Serves the historical CSV file for download, with fallback to RAM buffer.
    """
    try:
        # Tenta ler o ficheiro físico primeiro se ele existir na raiz
        file_path = BASE_DIR.parent / "history.csv"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return Response(
                body=content,
                status_code=200,
                headers={
                    "Content-Type": "text/csv",
                    "Content-Disposition": 'attachment; filename="historico_estacao.csv"',
                },
            )

        # Se não existir, gera o CSV a partir dos dados em RAM do buffer
        csv_content = "timestamp,temperatura,umidade,pressao,qualidade_ar\n"
        if _storage_buffer:
            for item in _storage_buffer.get_all():
                # Tratamento seguro para extração dos dicionários internos
                temp = item.get("temperature")
                temp_val = temp.get("value") if isinstance(temp, dict) else temp

                hum = item.get("humidity")
                hum_val = hum.get("value") if isinstance(hum, dict) else hum

                pres = item.get("pressure")
                pres_val = pres.get("value") if isinstance(pres, dict) else pres

                aqi = item.get("air_quality_index")
                aqi_val = aqi.get("value") if isinstance(aqi, dict) else aqi

                csv_content += f"{item.get('timestamp')},{temp_val},{hum_val},{pres_val},{aqi_val}\n"

        return Response(
            body=csv_content,
            status_code=200,
            headers={
                "Content-Type": "text/csv",
                "Content-Disposition": 'attachment; filename="historico_estacao.csv"',
            },
        )
    except Exception as e:
        return Response(body=f"Erro interno ao gerar CSV: {e}", status_code=500)
