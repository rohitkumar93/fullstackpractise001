from fastapi import APIRouter, Depends
from backend.selection_service.service import DocumentSelectionService
from backend.selection_service.schemas import DocumentSelectionRequest, DocumentSelectionResponse

router = APIRouter()

@router.get("/", response_model=DocumentSelectionResponse)
def select_document(
    request: DocumentSelectionRequest,
    service: DocumentSelectionService = Depends()
):
    """
    Allows users to filter and specify which documents should be
    considered in the retrieval process.
    """
    return service.get_selected_documents(request)
