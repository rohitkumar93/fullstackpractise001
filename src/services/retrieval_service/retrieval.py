import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from ...backend.database.config import AsyncSessionLocal
from ...backend.database.models import SelectedDocument
from ..ingestion_service.embedding_generator import EmbeddingGenerator
import asyncio

class RetrievalService:
    """
    Handles retrieval of similar documents based on query embeddings.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    async def retrieve_relevant_docs(self, query: str, top_k: int = 5):
        """
        Converts the query into an embedding and retrieves the most similar documents asynchronously.
        """
        async with AsyncSessionLocal() as db:
            async with db.begin():
                # ✅ Run embedding generation in a separate thread (to avoid blocking)
                query_embedding = await asyncio.to_thread(
                    self.embedding_generator.generate_embedding, query
                )

                # ✅ Convert NumPy array to PostgreSQL-compatible format
                query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

                # ✅ Fetch selected document IDs asynchronously
                selected_ids = await db.execute(text("SELECT document_id FROM selected_documents;"))
                selected_ids = selected_ids.scalars().all()

                # ✅ Ensure selected_ids is not empty to prevent SQL errors
                if not selected_ids:
                    selected_ids = [-1]  # Dummy ID to avoid SQL failure

                # ✅ Execute the vector similarity search query
                search_query = text("""
                    SELECT document_id FROM embeddings
                    WHERE document_id = ANY(:selected_ids)
                    ORDER BY vector <-> CAST(:query_embedding AS vector)
                    LIMIT :top_k;
                """).execution_options(cacheable=False)

                results = await db.execute(
                    search_query,
                    {
                        "query_embedding": query_embedding_str,  # Pass as string
                        "top_k": top_k,
                        "selected_ids": selected_ids,
                    },
                )

                document_ids = results.scalars().all()
                return document_ids
    async def get_document_texts(self, document_ids: list[int]):
        """
        Fetches the actual document texts for the given document IDs.
        """
        async with AsyncSessionLocal() as db:
            async with db.begin():
                if not document_ids:
                    return []

                query = text("SELECT content FROM documents WHERE id = ANY(:document_ids);")
                results = await db.execute(query, {"document_ids": document_ids})
                return results.scalars().all()
