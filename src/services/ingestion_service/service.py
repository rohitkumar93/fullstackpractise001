from ..ingestion_service.embedding_generator import EmbeddingGenerator
from ...backend.database.config import SessionLocal
from ...backend.database.models import Document, Embedding
from sqlalchemy.ext.asyncio import AsyncSession

class DocumentIngestionService:
    """
    Handles document ingestion, embedding generation, and database storage.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    async def process_document(self, filename: str, content: str):
        """
        Stores document text and generates embeddings for search.
        """
        if isinstance(content, bytes):
            content = content.decode("utf-8")

        async with SessionLocal() as db:
            async with db.begin():
                # Store document metadata
                document = Document(filename=filename, content=content.encode("utf-8"))
                db.add(document)
                await db.flush()  # Ensure document.id is available

                # Generate and store embeddings
                embedding_vector = self.embedding_generator.generate_embedding(content)
                embedding_entry = Embedding(document_id=document.id, vector=embedding_vector)
                db.add(embedding_entry)

            await db.commit()

        return {"message": "Document processed successfully"}
