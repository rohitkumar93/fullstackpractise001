import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.services.selection_service.service import DocumentSelectionService
from src.services.selection_service.schemas import DocumentSelectionRequest, DocumentSelectionResponse
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_selected_documents():
    service = DocumentSelectionService()
    
    # Mock the database session and query result.
    with patch.object(AsyncSession, 'execute', new_callable=AsyncMock) as mock_execute:
        mock_scalars = MagicMock()  # Use MagicMock instead of AsyncMock
        mock_scalars.all.return_value = [1, 2, 3]  # Mock the return value of all()
        mock_execute.return_value = MagicMock(scalars=lambda: mock_scalars)
        
        response = await service.get_selected_documents()
        assert response.selected_documents == ["1", "2", "3"]

@pytest.mark.asyncio
async def test_add_selected_documents():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=["1", "2", "3"])  # Pass strings instead of integers
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.add_selected_documents(request)
        assert response == {"message": "Documents selected successfully"}

@pytest.mark.asyncio
async def test_remove_selected_documents():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=["1", "2", "3"])  # Pass strings instead of integers
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.remove_selected_documents(request)
        assert response == {"message": "Documents removed from selection"}

# Additional tests
@pytest.mark.asyncio
async def test_get_selected_documents_no_documents():
    service = DocumentSelectionService()
    
    # Mock the database session and query result to return an empty list.
    with patch.object(AsyncSession, 'execute', new_callable=AsyncMock) as mock_execute:
        mock_scalars = MagicMock()  # Use MagicMock instead of AsyncMock
        mock_scalars.all.return_value = []  # Mock the return value of all()
        mock_execute.return_value = MagicMock(scalars=lambda: mock_scalars)
        
        response = await service.get_selected_documents()
        assert response.selected_documents == []

@pytest.mark.asyncio
async def test_add_selected_documents_empty_request():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=[])  # Empty list of document IDs
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.add_selected_documents(request)
        assert response == {"message": "Documents selected successfully"}

@pytest.mark.asyncio
async def test_remove_selected_documents_empty_request():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=[])  # Empty list of document IDs
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.remove_selected_documents(request)
        assert response == {"message": "Documents removed from selection"}

@pytest.mark.asyncio
async def test_add_selected_documents_duplicate_ids():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=["1", "1", "2", "2"])  # Duplicate document IDs
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.add_selected_documents(request)
        assert response == {"message": "Documents selected successfully"}

@pytest.mark.asyncio
async def test_remove_selected_documents_non_existent_ids():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=["99", "100"])  # Non-existent document IDs
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        response = await service.remove_selected_documents(request)
        assert response == {"message": "Documents removed from selection"}

            
@pytest.mark.asyncio
async def test_get_selected_documents_invalid_response():
    service = DocumentSelectionService()
    
    # Mock the database session to return invalid data.
    with patch.object(AsyncSession, 'execute', new_callable=AsyncMock) as mock_execute:
        mock_scalars = MagicMock()  # Use MagicMock instead of AsyncMock
        mock_scalars.all.return_value = [None, "invalid", 123]  # Mock the return value of all()
        mock_execute.return_value = MagicMock(scalars=lambda: mock_scalars)
        
        response = await service.get_selected_documents()
        assert response.selected_documents == ["None", "invalid", "123"]

@pytest.mark.asyncio
async def test_add_selected_documents_invalid_ids():
    service = DocumentSelectionService()
    request = DocumentSelectionRequest(document_ids=["invalid", "ids"])  # Invalid document IDs
    
    # Mock the database session.
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.__aenter__.return_value = mock_db
    mock_db.__aexit__.return_value = None
    mock_db.begin.return_value = AsyncMock(
        __aenter__=AsyncMock(return_value=None),
        __aexit__=AsyncMock(return_value=None)
    )
    
    with patch("src.services.selection_service.service.AsyncSessionLocal", return_value=mock_db):
        with pytest.raises(ValueError):
            await service.add_selected_documents(request)