from sqlalchemy.sql import text
from src.backend.database.config import AsyncSessionLocal
from src.services.ingestion_service.embedding_generator import EmbeddingGenerator


class RetrievalService:
    """
    Handles retrieval of similar documents based on query embeddings.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    async def retrieve_relevant_docs(self, question: str, top_k: int = 5):
        """
        Converts the query into an embedding and retrieves the most similar documents asynchronously.
        """
        async with AsyncSessionLocal() as db:
            async with db.begin():
                # ✅ Generate embedding in a separate thread
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
                print("selected_ids_result", vars(selected_ids_result))

                selected_ids = selected_ids_result.scalars().all()
                # selected_ids = (await selected_ids_result.scalars()).all()

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

                # document_ids = (await results.scalars()).all()\
                print("debug results", vars(results))
                # document_ids = list(await results.scalars())
                document_ids = list(results.scalars())

                print("document_ids", document_ids)
                return document_ids

    async def get_document_texts(self, document_ids: list[int]):
        """
        Fetches the actual document texts for the given document IDs.
        """
        if not document_ids:
            return []

        async with AsyncSessionLocal() as db:
            async with db.begin():
                question = text(
                    "SELECT content FROM documents WHERE id = ANY(:document_ids);"
                )
                results = await db.execute(question, {"document_ids": document_ids})
                # return (await results.scalars()).all()
                print("debug results", vars(results))
                return results.scalars().all()
