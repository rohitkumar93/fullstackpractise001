import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.retrieval_service.retrieval import RetrievalService
from sqlalchemy.ext.asyncio import AsyncSession



@pytest.mark.asyncio
async def test_retrieve_relevant_docs():
    # Mock the EmbeddingGenerator to avoid real model calls
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])

    # Mock the database session and transaction
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Mock the execute chain for both database calls
    # First call: SELECT document_id FROM selected_documents
    mock_selected_execute = MagicMock()
    mock_selected_scalars = MagicMock()
    mock_selected_scalars.all.return_value = [1, 2, 3]  # Selected IDs
    mock_selected_execute.scalars.return_value = mock_selected_scalars

    # Second call: Vector similarity search
    mock_search_execute = MagicMock()
    mock_search_scalars = MagicMock()
    mock_search_scalars.__iter__.return_value = iter([1, 2, 3])  # Document IDs
    mock_search_execute.scalars.return_value = mock_search_scalars

    # Configure execute to return different mocks for each call
    mock_db.execute.side_effect = [mock_selected_execute, mock_search_execute]

    # Mock async context managers
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = MagicMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )

    # Patch dependencies
    with patch(
        "src.services.retrieval_service.retrieval.AsyncSessionLocal", 
        return_value=mock_db
    ), patch(
        "src.services.retrieval_service.retrieval.EmbeddingGenerator", 
        return_value=mock_embedding_generator
    ):
        retrieval_service = RetrievalService()
        result = await retrieval_service.retrieve_relevant_docs("test query", 3)
        
        # Verify the returned document IDs
        assert result == [1, 2, 3]

@pytest.mark.asyncio
async def test_get_document_texts():
    # Mock the database session (AsyncSession)
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the async context manager methods (__aenter__ and __aexit__)
    mock_db.__aenter__.return_value = mock_db  # __aenter__ should return the mock_db itself
    mock_db.__aexit__.return_value = None  # __aexit__ should return None

    # Mock the execute method and its chain (scalars, all)
    mock_execute_result = MagicMock()  # Use MagicMock for scalars() and all()
    mock_scalars_result = MagicMock()
    mock_scalars_result.all.return_value = ["doc1", "doc2", "doc3"]  # Mock the return value of all()
    mock_execute_result.scalars.return_value = mock_scalars_result  # Mock the return value of scalars()
    mock_db.execute.return_value = mock_execute_result  # Mock the return value of execute()

    # Patch the AsyncSessionLocal to return the mock_db
    with patch("src.services.retrieval_service.retrieval.AsyncSessionLocal", return_value=mock_db):
        # Create an instance of RetrievalService
        retrieval_service = RetrievalService()

        # Call the method with the correct arguments (document_ids)
        document_texts = await retrieval_service.get_document_texts([1, 2, 3])

    # Debugging
    print("Final document_texts:", document_texts)

    # Assert the result
    assert document_texts == ["doc1", "doc2", "doc3"]  # This should now pass

@pytest.mark.asyncio
async def test_retrieve_relevant_docs_no_selected_docs():
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])

    mock_db = AsyncMock(spec=AsyncSession)

    # First call: Empty selected documents
    mock_selected_execute = MagicMock()
    mock_selected_scalars = MagicMock()
    mock_selected_scalars.all.return_value = []  # No selected document IDs
    mock_selected_execute.scalars.return_value = mock_selected_scalars

    # Second call: No search results
    mock_search_execute = MagicMock()
    mock_search_scalars = MagicMock()
    mock_search_scalars.__iter__.return_value = iter([])  # No retrieved document IDs
    mock_search_execute.scalars.return_value = mock_search_scalars

    mock_db.execute.side_effect = [mock_selected_execute, mock_search_execute]

    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = MagicMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )

    with patch("src.services.retrieval_service.retrieval.AsyncSessionLocal", return_value=mock_db), \
         patch("src.services.retrieval_service.retrieval.EmbeddingGenerator", return_value=mock_embedding_generator):
        retrieval_service = RetrievalService()
        result = await retrieval_service.retrieve_relevant_docs("test query", 3)

        # Expecting an empty list since no documents were selected
        assert result == []

@pytest.mark.asyncio
async def test_get_document_texts_empty_list():
    retrieval_service = RetrievalService()

    # No need to mock the DB because the function should return early
    result = await retrieval_service.get_document_texts([])

    # Expecting an empty list since there are no document IDs to retrieve
    assert result == []

@pytest.mark.asyncio
async def test_retrieve_relevant_docs_invalid_embedding():
    # Mock the EmbeddingGenerator to return an invalid embedding
    mock_embedding_generator = MagicMock()
    mock_embedding_generator.generate_embedding = AsyncMock(return_value=None)  # Invalid embedding

    # Mock the database session (AsyncSession)
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the async context manager methods (__aenter__ and __aexit__)
    mock_db.__aenter__.return_value = mock_db  # __aenter__ should return the mock_db itself
    mock_db.__aexit__.return_value = None  # __aexit__ should return None

    # Mock the begin() method to return an async context manager
    mock_transaction = AsyncMock()
    mock_transaction.__aenter__.return_value = None
    mock_transaction.__aexit__.return_value = None
    mock_db.begin.return_value = mock_transaction

    # Patch the AsyncSessionLocal to return the mock_db
    with patch("src.services.retrieval_service.retrieval.AsyncSessionLocal", return_value=mock_db), \
         patch("src.services.retrieval_service.retrieval.EmbeddingGenerator", return_value=mock_embedding_generator):
        # Create an instance of RetrievalService
        retrieval_service = RetrievalService()

        # Call the method with the correct arguments (question and top_k)
        result = await retrieval_service.retrieve_relevant_docs("test query", 3)

    # Expecting an empty list since the embedding was invalid
    assert result == []

@pytest.mark.asyncio
async def test_get_document_texts_no_matching_docs():
    # Mock the database session (AsyncSession)
    mock_db = AsyncMock(spec=AsyncSession)

    # Mock the async context manager methods (__aenter__ and __aexit__)
    mock_db.__aenter__.return_value = mock_db  # __aenter__ should return the mock_db itself
    mock_db.__aexit__.return_value = None  # __aexit__ should return None

    # Mock the begin() method to return an async context manager
    mock_transaction = AsyncMock()
    mock_transaction.__aenter__.return_value = None
    mock_transaction.__aexit__.return_value = None
    mock_db.begin.return_value = mock_transaction

    # Mock the execute method and its chain (scalars, all)
    mock_execute_result = MagicMock()
    mock_scalars_result = MagicMock()
    mock_scalars_result.all.return_value = []  # No matching documents
    mock_execute_result.scalars.return_value = mock_scalars_result
    mock_db.execute.return_value = mock_execute_result

    # Patch the AsyncSessionLocal to return the mock_db
    with patch("src.services.retrieval_service.retrieval.AsyncSessionLocal", return_value=mock_db):
        # Create an instance of RetrievalService
        retrieval_service = RetrievalService()

        # Call the method with the correct arguments (document_ids)
        document_texts = await retrieval_service.get_document_texts([99, 100])  # Non-existent IDs

    # Expecting an empty list since there are no matching documents
    assert document_texts == []
    