from fastapi import APIRouter, Depends
from backend.ingestion_service.service import DocumentIngestionService
from backend.ingestion_service.schemas import DocumentUploadRequest, DocumentUploadResponse

router = APIRouter()

# Inject service dependency for better testability and adherence to Dependency Inversion
@router.post("/", response_model=DocumentUploadResponse)
def ingest_document(
    request: DocumentUploadRequest,
    service: DocumentIngestionService = Depends()
):
    """
    Handles document ingestion by extracting text, generating embeddings,
    and storing them in the vector database.
    """
    return service.process_document(request)
