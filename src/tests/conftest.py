import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client