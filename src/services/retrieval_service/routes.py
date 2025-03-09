from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .retrieval import RetrievalService
from .bm25_retrieval import BM25RetrievalService  # ✅ Import BM25 retrieval service

import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()


# ✅ Define a Pydantic model for request validation
class QueryRequest(BaseModel):
    question: str
    top_k: int = 5  # Default value


# ✅ Embedding-based retrieval route
@router.post("/search/")
async def retrieve_documents(
    request: QueryRequest, service: RetrievalService = Depends()
):
    """
    Accepts a user query, retrieves the most relevant documents using embeddings,
    and returns matching document contents.
    """

    # ✅ Debug: Print the received request
    logger.debug(f"Received Request: {request}")

    results = await service.retrieve_relevant_docs(request.question, request.top_k)

    # ✅ Debug: Print the retrieved documents
    logger.debug(f"Retrieved Documents (Embedding): {results}")

    return {"documents": results}


# ✅ BM25-based retrieval route
@router.post("/search/bm25")
async def retrieve_documents_bm25(
    request: QueryRequest, service: BM25RetrievalService = Depends()
):
    """
    Accepts a user query, retrieves the most relevant documents using BM25 ranking,
    and returns matching document contents.
    """

    # ✅ Debug: Print the received request
    logger.debug(f"Received Request (BM25): {request}")
   
    results = await service.retrieve_relevant_docs(request.question, request.top_k)

    # ✅ Debug: Print the retrieved documents
    logger.debug(f"Retrieved Documents (BM25): {results}")

    return {"documents": results}
