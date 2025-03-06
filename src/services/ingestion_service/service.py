from src.services.ingestion_service.schemas import DocumentUploadRequest
from ..ingestion_service.embedding_generator import EmbeddingGenerator
from ...backend.database.config import AsyncSessionLocal
from ...backend.database.models import Document, Embedding
import asyncio


class DocumentIngestionService:
    """
    Handles document ingestion, embedding generation, and database storage.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    async def process_document(self, filename: str, content: str | bytes):
        """
        Stores document text and generates embeddings asynchronously.
        """
        if content is None:
            raise ValueError("Document content cannot be None")

        if isinstance(content, bytes):
            content = content.decode("utf-8")  # Convert bytes to string

        async with AsyncSessionLocal() as db:
            async with db.begin():
                document = Document(filename=filename, content=content.encode("utf-8"))
                db.add(document)
                await db.flush()  # Ensure document.id is available

                # Ensure embedding generation is awaited correctly
                embedding_vector = await asyncio.to_thread(
                    lambda: self.embedding_generator.generate_embedding(content)
                )

                # Ensure result is valid
                if not isinstance(embedding_vector, list) or not all(
                    isinstance(val, (float, int)) for val in embedding_vector
                ):
                    raise TypeError("Embedding vector must be a list of floats/ints.")

                # Create embedding entry
                embedding_entry = Embedding(
                    document_id=document.id, vector=embedding_vector
                )
                db.add(embedding_entry)

            await db.commit()

        return {"message": "Document processed successfully"}
