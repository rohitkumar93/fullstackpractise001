from sqlalchemy.sql import text  # Import SQL utilities for executing raw queries
from src.backend.database.config import (
    AsyncSessionLocal,
)  # Import async database session
from src.services.ingestion_service.embedding_generator import (
    EmbeddingGenerator,
)  # Import embedding generator


class RetrievalService:
    """
    Handles retrieval of similar documents based on query embeddings.
    """

    def __init__(self):
        self.embedding_generator = (
            EmbeddingGenerator()
        )  # Initialize embedding generator instance

    async def retrieve_relevant_docs(self, question: str, top_k: int = 5):
        """
        Converts the query into an embedding and retrieves the most similar documents asynchronously.
        - Generates an embedding for the query.
        - Retrieves selected document IDs from the database.
        - Performs vector similarity search to find the closest matches.
        """
        async with AsyncSessionLocal() as db:  # Open async database session
            async with db.begin():  # Start a database transaction
                # ✅ Generate embedding asynchronously
                query_embedding = await self.embedding_generator.generate_embedding(
                    question
                )

                # Handle invalid embedding
                if query_embedding is None:
                    return []

                # ✅ Convert NumPy array to PostgreSQL-compatible format
                query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

                # ✅ Fetch selected document IDs asynchronously
                selected_ids_result = await db.execute(
                    text("SELECT document_id FROM selected_documents;")
                )

                selected_ids = selected_ids_result.scalars().all()

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

                # ✅ Extract document IDs from query results
                document_ids = list(results.scalars())
                return document_ids

    async def get_document_texts(self, document_ids: list[int]):
        """
        Fetches the actual document texts for the given document IDs.
        """
        if not document_ids:
            return []  # Return empty list if no document IDs provided

        async with AsyncSessionLocal() as db:  # Open async database session
            async with db.begin():  # Start a transaction
                question = text(
                    "SELECT content FROM documents WHERE id = ANY(:document_ids);"
                )
                results = await db.execute(question, {"document_ids": document_ids})
                return results.scalars().all()  # Return list of document contents
