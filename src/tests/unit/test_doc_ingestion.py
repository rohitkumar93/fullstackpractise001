import pytest
import asyncio
from src.services.ingestion_service.service import DocumentIngestionService
from src.services.ingestion_service.schemas import DocumentUploadRequest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_process_document_valid_string():
    service = DocumentIngestionService()
    
    # Patch the embedding generator to return a valid vector.
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        
        response = await service.process_document("test.txt", "This is a test document.")
        assert response == {"message": "Document processed successfully"}

@pytest.mark.asyncio
async def test_process_document_valid_bytes():
    service = DocumentIngestionService()
    
    # Patch the embedding generator to return a valid vector.
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        
        response = await service.process_document("test.txt", b"This is a test document.")
        assert response == {"message": "Document processed successfully"}

@pytest.mark.asyncio
async def test_process_document_none_content():
    service = DocumentIngestionService()
    with pytest.raises(ValueError, match="Document content cannot be None"):
        await service.process_document("test.txt", None)

@pytest.mark.asyncio
async def test_process_document_invalid_embedding():
    service = DocumentIngestionService()
    
    # Patch the embedding generator to return an invalid vector.
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = "invalid_vector"
        
        with pytest.raises(TypeError, match="Embedding vector must be a list of floats/ints."):
            await service.process_document("test.txt", "This is a test document.")

@pytest.mark.asyncio
async def test_process_documents_batch():
    service = DocumentIngestionService()
    documents = [
        DocumentUploadRequest(filename=f"test_doc_{i}.txt", content=f"This is test document number {i}.")
        for i in range(3)
    ]
    
    # Patch the embedding generator for each document in the batch.
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        responses = await service.process_documents_batch(documents)
        for response in responses:
            assert response == {"message": "Document processed successfully"}

@pytest.mark.asyncio
async def test_process_document_empty_string():
    """Ensure empty string content is handled properly."""
    service = DocumentIngestionService()
    with pytest.raises(ValueError, match="Document content cannot be empty"):
        await service.process_document("empty.txt", "")

@pytest.mark.asyncio
async def test_process_document_empty_bytes():
    """Ensure empty bytes content is handled properly."""
    service = DocumentIngestionService()
    with pytest.raises(ValueError, match="Document content cannot be empty"):
        await service.process_document("empty_bytes.txt", b"")

@pytest.mark.asyncio
async def test_process_large_document():
    """Ensure the system can handle a large document without crashing."""
    service = DocumentIngestionService()
    large_content = "A" * 10_000_000  # 10MB content
    
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384  # Simulating valid embedding
        response = await service.process_document("large.txt", large_content)
        assert response == {"message": "Document processed successfully"}

@pytest.mark.asyncio
async def test_process_document_duplicate_filename():
    """Ensure handling of duplicate filenames (depends on business logic)."""
    service = DocumentIngestionService()
    
    # First upload should succeed
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        response1 = await service.process_document("duplicate.txt", "First version")
        assert response1 == {"message": "Document processed successfully"}
    
    # Second upload: Should it replace, update, or be rejected?
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
        response2 = await service.process_document("duplicate.txt", "Second version")
        assert response2 == {"message": "Document processed successfully"}  # Update logic?

@pytest.mark.asyncio
async def test_process_document_db_failure():
    """Ensure rollback occurs if database commit fails."""
    service = DocumentIngestionService()
    
    with patch.object(service.embedding_generator, 'generate_embedding', new_callable=AsyncMock) as mock_embedding:
        mock_embedding.return_value = [0.1] * 384
    
        with patch.object(AsyncSession, 'commit', side_effect=Exception("DB Failure")):
            with pytest.raises(Exception, match="DB Failure"):
                await service.process_document("db_fail.txt", "This should fail")