import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_valid_question(async_client: AsyncClient):
    response = await async_client.post("/qna/ask", json={"query": "What is AI?"})
    assert response.status_code == 200
    assert "answer" in response.json()

@pytest.mark.asyncio
async def test_invalid_question(async_client: AsyncClient):
    response = await async_client.post("/qna/ask", json={})  # Missing query
    assert response.status_code == 422  # Unprocessable Entity
