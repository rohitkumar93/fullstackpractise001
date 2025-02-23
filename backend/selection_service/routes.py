from fastapi import APIRouter, Depends
from backend.selection_service.service import DocumentSelectionService
from backend.selection_service.schemas import DocumentSelectionRequest, DocumentSelectionResponse

router = APIRouter()

@router.get("/", response_model=DocumentSelectionResponse)
def get_selected_documents(service: DocumentSelectionService = Depends()):
    """
    Retrieves the list of currently selected documents.
    """
    return service.get_selected_documents()

@router.post("/add")
def add_selected_documents(
    request: DocumentSelectionRequest,
    service: DocumentSelectionService = Depends()
):
    """
    Adds documents to the selection list.
    """
    return service.add_selected_documents(request)

@router.post("/remove")
def remove_selected_documents(
    request: DocumentSelectionRequest,
    service: DocumentSelectionService = Depends()
):
    """
    Removes documents from the selection list.
    """
    return service.remove_selected_documents(request)
