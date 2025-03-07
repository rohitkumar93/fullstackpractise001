import pytest
import asyncio
from unittest.mock import patch, MagicMock
from src.services.ingestion_service.embedding_generator import EmbeddingGenerator

@pytest.fixture
def embedding_generator():
    """Fixture to initialize EmbeddingGenerator."""
    return EmbeddingGenerator()

@pytest.mark.asyncio
async def test_generate_embedding_valid_text(embedding_generator):
    """Test generating embedding for valid text."""
    text = "This is a test document."
    embedding = await embedding_generator.generate_embedding(text)
    assert isinstance(embedding, list)
    assert all(isinstance(val, float) for val in embedding)

@pytest.mark.asyncio
async def test_generate_embedding_empty_text(embedding_generator):
    """Test generating embedding for empty text."""
    text = ""
    embedding = await embedding_generator.generate_embedding(text)
    assert isinstance(embedding, list)
    assert all(isinstance(val, float) for val in embedding)

@pytest.mark.asyncio
async def test_generate_embedding_long_text(embedding_generator):
    """Test generating embedding for a long text."""
    text = "This is a test document." * 1000  # Long text
    embedding = await embedding_generator.generate_embedding(text)
    assert isinstance(embedding, list)
    assert all(isinstance(val, float) for val in embedding)

@pytest.mark.asyncio
async def test_generate_embedding_special_characters(embedding_generator):
    """Test generating embedding for text with special characters."""
    text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    embedding = await embedding_generator.generate_embedding(text)
    assert isinstance(embedding, list)
    assert all(isinstance(val, float) for val in embedding)

@pytest.mark.asyncio
async def test_generate_embedding_mocked(embedding_generator):
    """Test generating embedding with mocked tokenizer and model."""
    text = "This is a test document."

    with patch.object(embedding_generator.tokenizer, 'from_pretrained', return_value=MagicMock()) as mock_tokenizer, \
         patch.object(embedding_generator.model, 'from_pretrained', return_value=MagicMock()) as mock_model:
        
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        
        embedding = await embedding_generator.generate_embedding(text)
        assert isinstance(embedding, list)
        assert all(isinstance(val, float) for val in embedding)