import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.backend.database.config import AsyncSessionLocal
from src.backend.database.models import Document, Embedding
from src.services.ingestion_service.service import DocumentIngestionService

@pytest.mark.asyncio
async def test_process_document_success():
    """Test successful document ingestion with mocked embedding generation."""
    service = DocumentIngestionService()

    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        
        response = await service.process_document("test.txt", "This is a test document.")
        assert response["message"] == "Document processed successfully"


@pytest.mark.asyncio
async def test_process_document_bytes_input():
    """Test handling of byte input.""""" 
    service = DocumentIngestionService()

    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        
        response = await service.process_document("test.txt", b"Byte content test")
        assert response["message"] == "Document processed successfully"


@pytest.mark.asyncio
async def test_process_document_none_content():
    """Test that None content raises a ValueError."""
    service = DocumentIngestionService()
    
    with pytest.raises(ValueError, match="Document content cannot be None"):
        await service.process_document("test.txt", None)


@pytest.mark.asyncio
async def test_process_document_invalid_embedding():
    """Test handling of an invalid embedding result."""
    service = DocumentIngestionService()

    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = "invalid_data"
        
        with pytest.raises(TypeError, match="Embedding vector must be a list of floats/ints"):
            await service.process_document("test.txt", "Valid content")


@pytest.mark.asyncio
async def test_process_document_integration():
    """Full integration test using the actual database and embedding generator."""
    service = DocumentIngestionService()
    async with AsyncSessionLocal() as session:
        # Clear database before test
        await session.execute(Document.__table__.delete())
        await session.execute(Embedding.__table__.delete())
        await session.commit()

        response = await service.process_document("integration_test.txt", "Integration test content")
        assert response["message"] == "Document processed successfully"

        # Verify database insertions
        result = await session.execute(Document.__table__.select())
        document = result.scalars().first()
        assert document is not None
        assert document.filename == "integration_test.txt"

        result = await session.execute(Embedding.__table__.select())
        embedding = result.scalars().first()
        assert embedding is not None
        assert len(embedding.vector) == 384
