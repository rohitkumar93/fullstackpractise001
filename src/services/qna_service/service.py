import openai
import os
from ..retrieval_service.retrieval import RetrievalService
from ..retrieval_service.schemas import QueryRequest, QueryResponse

class QnAService:
    """
    Handles Q&A functionality by retrieving relevant documents and generating an answer.
    """

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # ✅ Store API key in environment variables

    async def get_answer(self, request: QueryRequest) -> QueryResponse:
        """
        Retrieves the most relevant documents and generates an answer
        using OpenAI GPT API.
        """
        # ✅ Step 1: Retrieve relevant document IDs
        document_ids = await self.retrieval_service.retrieve_relevant_docs(request.query, request.top_k)

        # ✅ Step 2: Fetch actual document texts
        document_texts = await self.retrieval_service.get_document_texts(document_ids)

        # ✅ Step 3: Format documents for LLM input
        doc_texts = "\n\n".join(doc.decode("utf-8") if isinstance(doc, bytes) else str(doc) for doc in document_texts) if document_texts else "No relevant documents found."

        # ✅ Step 4: Call OpenAI API to generate answer
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert answering questions based on retrieved documents."},
                {"role": "user", "content": f"Context:\n{doc_texts}\n\nQuestion: {request.query}\nAnswer:"}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # ✅ Step 5: Extract and return the generated answer
        answer = response["choices"][0]["message"]["content"]
        print("DEBUG: Answer received from OpenAI:", answer)
        

        return QueryResponse(answer=answer)
