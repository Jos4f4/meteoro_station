"""
Integration tests for the web server API endpoints.
"""

import pytest
from microdot.test_client import TestClient

from src.core.storage import CircularBuffer
from src.web.server import init_app


@pytest.fixture
def mock_buffer():
    """
    Provides a populated buffer for API testing.
    """

    buffer = CircularBuffer(capacity=5)
    buffer.add_reading({
        "timestamp": 1726876543,
        "temperature": 31.4,
        "humidity": 78.0,
        "pressure": 1012.0,
        "air_quality_index": 120.5,
        "gas_state": "valid"
    })

    return buffer


@pytest.fixture
def test_client(mock_buffer):
    """
    Provides the Microdot test client with the injected buffer.
    """

    app = init_app(mock_buffer)
    
    return TestClient(app)


@pytest.mark.asyncio
async def test_serve_index_returns_html(test_client):
    """
    Ensures that the root route successfully returns the dashboard HTML.
    """

    response = await test_client.get('/')

    assert response.status_code == 200, f"Failure: {response.body}"
    assert 'text/html' in response.headers['Content-Type']
    assert b'Meteoro Station' in response.body  


@pytest.mark.asyncio
async def test_serve_static_js(test_client):
    """
    Ensures that the static route correctly returns the frontend script.
    """

    response = await test_client.get('/static/app.js')
    
    assert response.status_code == 200, f"Failure: {response.body}"
    assert 'application/javascript' in response.headers['Content-Type']
    assert b'fetchReadings()' in response.body
