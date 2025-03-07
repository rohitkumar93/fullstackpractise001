from rank_bm25 import BM25Okapi
from src.backend.database.config import AsyncSessionLocal
from src.backend.database.models import Document, SelectedDocument
from typing import List
import nltk

# nltk.download()
# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download("omw-1.4")


def tokenize(text: str) -> List[str]:
    """Tokenizes and preprocesses text for BM25."""
    return nltk.word_tokenize(text.lower())


class BM25RetrievalService:
    """
    Handles document retrieval using BM25 ranking.
    """

    def __init__(self):
        self.documents = []  # Store tokenized documents
        self.doc_ids = []  # Map document order to IDs
        self.bm25 = None  # BM25 model
        self.load_documents()

    def load_documents(self):
        """Loads and tokenizes documents from the database."""
        db = AsyncSessionLocal()
        try:
            selected_ids = db.query(SelectedDocument.document_id).all()
            selected_ids = [row[0] for row in selected_ids] if selected_ids else []

            if not selected_ids:
                return

            docs = db.query(Document).filter(Document.id.in_(selected_ids)).all()

            self.documents = [tokenize(doc.content.decode("utf-8")) for doc in docs]
            self.doc_ids = [doc.id for doc in docs]

            if self.documents:
                self.bm25 = BM25Okapi(self.documents)
        finally:
            db.close()

    def retrieve_relevant_docs(self, question: str, top_k: int = 5) -> List[int]:
        """Retrieves top-k relevant documents using BM25 scoring."""
        if not self.bm25 or not question.strip():
            return []

        tokenized_query = tokenize(question)
        scores = self.bm25.get_scores(tokenized_query)

        sorted_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )
        top_doc_ids = [self.doc_ids[i] for i in sorted_indices[:top_k]]

        return top_doc_ids
