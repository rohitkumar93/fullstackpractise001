import pytest
import os
from unittest.mock import patch, AsyncMock
from src.services.qna_service.service import QnAService
from src.services.qna_service.schemas import QueryRequest


@pytest.mark.asyncio
async def test_get_answer_valid_query():
    service = QnAService()
    request = QueryRequest(question="What is AI?", top_k=3)

    # Patch the retrieval service to return mock document IDs and texts.
    with (
        patch.object(
            service.retrieval_service, "retrieve_relevant_docs", new_callable=AsyncMock
        ) as mock_retrieve_docs,
        patch.object(
            service.retrieval_service, "get_document_texts", new_callable=AsyncMock
        ) as mock_get_texts,
        patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai,
    ):
        mock_retrieve_docs.return_value = [1, 2, 3]
        mock_get_texts.return_value = [
            "Document 1 text",
            "Document 2 text",
            "Document 3 text",
        ]
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "AI is the simulation of human intelligence in machines."
                    }
                }
            ]
        }

        response = await service.get_answer(request)
        assert (
            response.answer == "AI is the simulation of human intelligence in machines."
        )


@pytest.mark.asyncio
async def test_get_answer_no_relevant_docs():
    service = QnAService()
    request = QueryRequest(question="What is AI?", top_k=3)

    # Patch the retrieval service to return no document IDs.
    with (
        patch.object(
            service.retrieval_service, "retrieve_relevant_docs", new_callable=AsyncMock
        ) as mock_retrieve_docs,
        patch.object(
            service.retrieval_service, "get_document_texts", new_callable=AsyncMock
        ) as mock_get_texts,
        patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai,
    ):
        mock_retrieve_docs.return_value = []
        mock_get_texts.return_value = []
        mock_openai.return_value = {
            "choices": [{"message": {"content": "No relevant documents found."}}]
        }

        response = await service.get_answer(request)
        assert response.answer == "No relevant documents found."


def test_qna_service_missing_api_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
        with pytest.raises(ValueError, match="OpenAI API key is missing"):
            QnAService()
