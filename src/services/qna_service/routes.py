from fastapi import APIRouter, HTTPException, Depends
from .service import QnAService, RetrievalService
import logging
from .schemas import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
retrieval_service = RetrievalService()
qna_service = QnAService()

@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Handles user queries by retrieving relevant documents and generating answers using RAG.
    """
    try:
        # Retrieve relevant documents
        relevant_docs = await retrieval_service.retrieve_relevant_docs(request.query, request.top_k)

        if not relevant_docs:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # ✅ Await the async function call
        answer = await qna_service.get_answer(request)

        return QueryResponse(question=request.query, answer=str(answer))


    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
