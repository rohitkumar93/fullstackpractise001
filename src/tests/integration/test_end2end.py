import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_end_to_end_flow(async_client: AsyncClient):
    # Step 1: Ingest document
    doc_response = await async_client.post("/documents/ingest", json={"content": "Python is a programming language."})
    assert doc_response.status_code == 200
    doc_id = doc_response.json()["embedding_id"]

    # Step 2: Ask a question
    qna_response = await async_client.post("/qna/ask", json={"query": "What is Python?"})
    assert qna_response.status_code == 200
    assert "answer" in qna_response.json()
