from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .retrieval import RetrievalService

import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# ✅ Define a Pydantic model for request validation
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5  # Default value

@router.post("/search")
def retrieve_documents(request: QueryRequest, service: RetrievalService = Depends()):
    """
    Accepts a user query, retrieves the most relevant documents using embeddings,
    and returns matching document contents.
    """

    # ✅ Debug: Print the received request
    logger.debug(f"Received Request: {request}")
    print(f"✅ Received Request: {request}")  # Debugging print
    retrieval_service = RetrievalService()
    results = retrieval_service.retrieve_relevant_docs(request.query, request.top_k)

    # ✅ Debug: Print the retrieved documents
    logger.debug(f"Retrieved Documents: {results}")

    return {"documents": results}
