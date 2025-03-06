import pytest
import asyncio
from httpx import AsyncClient
from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Ensure a new event loop is used for Windows compatibility."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_client():
    """Fixture for creating an HTTP client for API testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client