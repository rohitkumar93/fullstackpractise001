import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_document_ingestion(async_client: AsyncClient):
    response = await async_client.post("/documents/ingest", json={"content": "Test document."})
    assert response.status_code == 200
    assert "embedding_id" in response.json()
