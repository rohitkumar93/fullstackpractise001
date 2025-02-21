from backend.ingestion_service.embedding_generator import EmbeddingGenerator
from backend.database.config import SessionLocal
from backend.database.models import Document
from sqlalchemy.sql import text
import numpy as np
from sqlalchemy.dialects.postgresql import ARRAY

class RetrievalService:
    """
    Handles retrieval of similar documents based on query embeddings.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    def search_similar_documents(self, query: str, top_k: int = 5):
        """
        Converts the query into an embedding and retrieves the most similar documents.
        """
        db = SessionLocal()

        # ✅ Convert query into an embedding
        query_embedding = self.embedding_generator.generate_embedding(query)

        # ✅ Ensure the embedding is a NumPy array before sending to PostgreSQL
        query_embedding = np.array(query_embedding, dtype=np.float32).tolist()

        # ✅ Convert query embedding to a `vector` type explicitly
        search_query = text("""
            SELECT document_id FROM embeddings
            ORDER BY vector <-> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """).execution_options(cacheable=False)

        print(f"Executing query: {search_query} with params: {query_embedding[0]}")

        # ✅ Execute the query
        results = db.execute(search_query, {"query_embedding": query_embedding, "top_k": top_k}).fetchall()
        document_ids = [row[0] for row in results]

        db.close()
        return document_ids
