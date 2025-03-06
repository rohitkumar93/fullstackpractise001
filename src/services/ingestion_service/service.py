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

    async def process_document(self, filename: str, content: str):
        """
        Stores document text and generates embeddings asynchronously.
        """
        if isinstance(content, bytes):
            content = content.decode("utf-8")

        async with SessionLocal() as db:
            async with db.begin():
                document = Document(filename=filename, content=content.encode("utf-8"))
                db.add(document)
                await db.flush()  # Ensure document.id is available

                # Run embedding generation and database insertion concurrently
                embedding_task = asyncio.to_thread(
                    self.embedding_generator.generate_embedding, content
                )
                db_commit_task = db.commit()  # Commit in parallel

                embedding_vector = (
                    await embedding_task
                )  # Wait for embedding computation

                # Create embedding entry
                embedding_entry = Embedding(
                    document_id=document.id, vector=embedding_vector
                )
                db.add(embedding_entry)

            await db_commit_task  # Ensure DB commit happens concurrently

        return {"message": "Document processed successfully"}

    async def process_documents_batch(self, documents: list[DocumentUploadRequest]):
        """
        Processes multiple documents concurrently using asyncio.gather.
        """
        tasks = [self.process_document(doc.filename, doc.content) for doc in documents]
        return await asyncio.gather(*tasks)  # Run all document ingestions in parallel
