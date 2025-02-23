from fastapi import APIRouter, Depends
from backend.ingestion_service.service import DocumentIngestionService
from backend.ingestion_service.schemas import DocumentUploadRequest, DocumentUploadResponse
from backend.ingestion_service.arxiv_ingester import fetch_arxiv_papers, store_papers_in_db


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

@router.post("/ingest_from_arxiv")
def ingest_papers(query: str = "negative impacts of PC gaming", limit: int = 5):
    """
    Fetches papers from ArXiv and stores them in the database.
    """
    papers = fetch_arxiv_papers(query, max_results=limit)
    store_papers_in_db(papers)
    return {"message": f"{len(papers)} papers ingested successfully!"}