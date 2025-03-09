import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock


@pytest.mark.asyncio
async def test_end_to_end_flow(async_client: AsyncClient):
    # Mock the EmbeddingGenerator to return a valid embedding vector
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3] * 128
    )

    # Patch the EmbeddingGenerator in the DocumentIngestionService
    with patch(
        "src.services.ingestion_service.service.EmbeddingGenerator",
        return_value=mock_embedding_generator,
    ):
        # Step 1: Ingest document
        doc_response = await async_client.post(
            "/ingestion/",
            json={
                "filename": "test_doc.txt",
                "content": "Python is a programming language.",
            },
        )
        assert doc_response.status_code == 200
        assert doc_response.json()["message"] == "Document processed successfully"

        # Step 2: Select the ingested document
        select_response = await async_client.post(
            "/selection/add", json={"document_ids": ["1"]}
        )
        assert select_response.status_code == 200
        assert select_response.json()["message"] == "Documents selected successfully"

        # Step 3: Retrieve the document based on embeddings
        retrieve_response = await async_client.post(
            "/retrieval/search/", json={"question": "Python", "top_k": 1}
        )
        assert retrieve_response.status_code == 200
        assert "documents" in retrieve_response.json()
        assert len(retrieve_response.json()["documents"]) > 0

        # Step 4: Perform Q&A operation based on the retrieved document
        qna_response = await async_client.post(
            "/qna/ask", json={"question": "What is Python?", "top_k": 1}
        )
        assert qna_response.status_code == 200
        assert "answer" in qna_response.json()
        assert qna_response.json()["answer"] is not None


@pytest.mark.asyncio
async def test_end_to_end_flow_with_multiple_documents(async_client: AsyncClient):
    # Mock the EmbeddingGenerator to return a valid embedding vector
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3] * 128
    )

    # Patch the EmbeddingGenerator in the DocumentIngestionService
    with patch(
        "src.services.ingestion_service.service.EmbeddingGenerator",
        return_value=mock_embedding_generator,
    ):
        # Step 1: Ingest multiple documents
        docs = [
            {"filename": "doc1.txt", "content": "Python is a programming language."},
            {"filename": "doc2.txt", "content": "Machine learning is a subset of AI."},
            {"filename": "doc3.txt", "content": "Deep learning uses neural networks."},
        ]
        for doc in docs:
            doc_response = await async_client.post("/ingestion/", json=doc)
            assert doc_response.status_code == 200
            assert doc_response.json()["message"] == "Document processed successfully"

        # Step 2: Select the ingested documents
        select_response = await async_client.post(
            "/selection/add", json={"document_ids": ["1", "2", "3"]}
        )
        assert select_response.status_code == 200
        assert select_response.json()["message"] == "Documents selected successfully"

        # Step 3: Retrieve the documents based on embeddings
        retrieve_response = await async_client.post(
            "/retrieval/search/", json={"question": "AI", "top_k": 3}
        )
        assert retrieve_response.status_code == 200
        assert "documents" in retrieve_response.json()
        assert len(retrieve_response.json()["documents"]) > 0

        # Step 4: Perform Q&A operation based on the retrieved documents
        qna_response = await async_client.post(
            "/qna/ask", json={"question": "What is AI?", "top_k": 3}
        )
        assert qna_response.status_code == 200
        assert "answer" in qna_response.json()
        assert qna_response.json()["answer"] is not None


@pytest.mark.asyncio
async def test_end_to_end_flow_with_arxiv_papers(async_client: AsyncClient):
    # Mock the EmbeddingGenerator to return a valid embedding vector
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(
        return_value=[0.1, 0.2, 0.3] * 128
    )

    # Patch the EmbeddingGenerator in the DocumentIngestionService
    with patch(
        "src.services.ingestion_service.service.EmbeddingGenerator",
        return_value=mock_embedding_generator,
    ):
        # Step 1: Ingest papers from ArXiv
        arxiv_response = await async_client.post(
            "/ingestion/ingest_from_arxiv",
            params={"question": "machine learning", "limit": 2},
        )
        assert arxiv_response.status_code == 200
        assert "message" in arxiv_response.json()

        # Step 2: Select the ingested papers
        select_response = await async_client.post(
            "/selection/add", json={"document_ids": ["1", "2"]}
        )
        assert select_response.status_code == 200
        assert select_response.json()["message"] == "Documents selected successfully"

        # Step 3: Retrieve the papers based on embeddings
        retrieve_response = await async_client.post(
            "/retrieval/search/", json={"question": "machine learning", "top_k": 2}
        )
        assert retrieve_response.status_code == 200
        assert "documents" in retrieve_response.json()
        assert len(retrieve_response.json()["documents"]) > 0

        # Step 4: Perform Q&A operation based on the retrieved papers
        qna_response = await async_client.post(
            "/qna/ask", json={"question": "What is machine learning?", "top_k": 2}
        )
        assert qna_response.status_code == 200
        assert "answer" in qna_response.json()
        assert qna_response.json()["answer"] is not None
