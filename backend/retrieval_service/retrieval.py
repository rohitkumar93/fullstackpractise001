import numpy as np
from sqlalchemy.sql import text
from backend.database.config import SessionLocal
from backend.database.models import SelectedDocument
from backend.ingestion_service.embedding_generator import EmbeddingGenerator


class RetrievalService:
    """
    Handles retrieval of similar documents based on query embeddings.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    def retrieve_relevant_docs(self, query: str, top_k: int = 5):
        """
        Converts the query into an embedding and retrieves the most similar documents.
        """
        db = SessionLocal()
        try:
            # ✅ Convert query to embedding
            query_embedding = self.embedding_generator.generate_embedding(query)
            query_embedding = np.array(query_embedding, dtype=np.float32).tolist()

            # ✅ Fetch selected document IDs
            selected_ids = db.query(SelectedDocument.document_id).all()
            selected_ids = [row[0] for row in selected_ids]  # Extract IDs

            # ✅ Ensure selected_ids is not empty
            if not selected_ids:
                selected_ids = [-1]  # Prevent SQL errors

            # ✅ Correct SQL Query: First order by similarity, then filter by selected_ids
            search_query = text("""
                SELECT document_id FROM embeddings
                WHERE document_id = ANY(:selected_ids)
                ORDER BY vector <-> (:query_embedding)::vector
                LIMIT :top_k;
            """).execution_options(cacheable=False)

            results = db.execute(
                search_query,
                {
                    "query_embedding": query_embedding,
                    "top_k": top_k,
                    "selected_ids": selected_ids,
                }
            ).fetchall()

            document_ids = [row[0] for row in results]
            return document_ids

        finally:
            db.close()  # ✅ Ensure DB connection is always closed
