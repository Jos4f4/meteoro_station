"""
Acceptance tests for the Microdot web server API endpoints.
Validates data retrieval and CSV export functionalities.
"""

import pytest
from microdot import Request

from src.core.storage import CircularBuffer
from src.web.server import init_app


@pytest.fixture
def client():
    """
    Pytest fixture that initializes the web application with a pre-populated
    RAM buffer for testing API endpoints.

    Returns:
        Microdot: The configured Microdot application instance.
    """
    buffer = CircularBuffer(capacity=5)
    buffer.add_reading({
        "timestamp": 1234567890,
        "temperature": 28.5,
        "humidity": 70.0,
        "pressure": 1013.2,
        "air_quality_index": 45.0,
        "gas_state": "valid"
    })
    return init_app(buffer)


@pytest.mark.asyncio
async def test_api_latest_endpoint(client):
    """
    Tests the '/api' endpoint to ensure it successfully returns
    the latest sensor readings (including specific data points like temperature) 
    with an HTTP 200 OK status.

    Args:
        client: The Microdot application fixture.
    """
    req = Request('GET', '/api', headers={}, query_string='', body=b'')
    res = await client.dispatch(req)
    
    assert res.status_code == 200
    assert b"28.5" in res.body


@pytest.mark.asyncio
async def test_api_export_csv_endpoint(client):
    """
    Tests the '/api/exportar.csv' endpoint to ensure it successfully generates 
    and returns the historical data in CSV format with an HTTP 200 OK status.

    Args:
        client: The Microdot application fixture.
    """
    req = Request('GET', '/api/exportar.csv', headers={}, query_string='', body=b'')
    res = await client.dispatch(req)
    
    assert res.status_code == 200
    assert b"timestamp" in res.body