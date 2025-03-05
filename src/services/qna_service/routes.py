from fastapi import APIRouter, HTTPException, Depends
import logging
# from services.qna_service.service import QnAService
# from services.retrieval_service.retrieval import RetrievalService

from .service import QnAService, RetrievalService

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
retrieval_service = RetrievalService()
qna_service = QnAService()


@router.post("/ask")
async def ask_question(question: str):
    """
    Handles user queries by retrieving relevant documents and generating answers using RAG.
    """
    logger.debug(f"📥 Received question: {question}")

    try:
        # Retrieve relevant documents
        relevant_docs = retrieval_service.retrieve_relevant_docs(question)
        logger.debug(f"🔍 Retrieved documents: {relevant_docs}")

        if not relevant_docs:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # Generate an answer using RAG
        answer = qna_service.get_answer(question, relevant_docs)
        logger.debug(f"📝 Generated answer: {answer}")

        return {"question": question, "answer": answer}

    except Exception as e:
        logger.error(f"❌ Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
