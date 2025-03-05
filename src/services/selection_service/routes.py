from fastapi import APIRouter, Depends
from src.services.selection_service.service import DocumentSelectionService
from src.services.selection_service.schemas import DocumentSelectionRequest, DocumentSelectionResponse

router = APIRouter()

@router.get("/", response_model=DocumentSelectionResponse)
async def get_selected_documents(service: DocumentSelectionService = Depends()):
    """
    Retrieves the list of selected documents.
    """
    return await service.get_selected_documents()

@router.post("/add", response_model=dict)
async def add_selected_documents(
    request: DocumentSelectionRequest,
    service: DocumentSelectionService = Depends()
):
    """
    Adds document IDs to the selection list.
    """
    return await service.add_selected_documents(request)

@router.post("/remove", response_model=dict)
async def remove_selected_documents(
    request: DocumentSelectionRequest,
    service: DocumentSelectionService = Depends()
):
    """
    Removes document IDs from the selection list.
    """
    return await service.remove_selected_documents(request)