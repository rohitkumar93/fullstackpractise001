from src.services.ingestion_service.schemas import (
    DocumentUploadRequest,
)  # Import schema for document upload request
from src.services.ingestion_service.embedding_generator import (
    EmbeddingGenerator,
)  # Import embedding generator
from src.backend.database.config import (
    AsyncSessionLocal,
)  # Import async database session
from src.backend.database.models import (
    Document,
    Embedding,
)  # Import ORM models for document and embedding

import asyncio  # Import asyncio for asynchronous operations


class DocumentIngestionService:
    """
    Handles document ingestion, embedding generation, and database storage.
    """

    def __init__(self):
        self.embedding_generator = (
            EmbeddingGenerator()
        )  # Initialize embedding generator instance

    async def process_document(self, filename: str, content: str | bytes):
        """
        Processes a single document:
        - Ensures content is valid.
        - Stores document in the database.
        - Generates an embedding vector.
        - Stores embedding in the database.
        """
        if content is None:
            raise ValueError(
                "Document content cannot be None"
            )  # Validate non-null content

        if isinstance(content, bytes):
            content = content.decode("utf-8")  # Convert bytes to UTF-8 string if needed

        if not content.strip():
            raise ValueError(
                "Document content cannot be empty"
            )  # Ensure content is not just whitespace

        async with AsyncSessionLocal() as db:  # Open async database session
            async with db.begin():  # Start a database transaction
                document = Document(
                    filename=filename, content=content.encode("utf-8")
                )  # Create document entry
                db.add(document)
                await db.flush()  # Ensure document.id is generated before using it

                # Generate embedding asynchronously
                embedding_vector = await self.embedding_generator.generate_embedding(
                    content
                )

                # Validate embedding vector format
                if not isinstance(embedding_vector, list) or not all(
                    isinstance(val, (float, int)) for val in embedding_vector
                ):
                    raise TypeError("Embedding vector must be a list of floats/ints.")

                # Create embedding entry linked to document
                embedding_entry = Embedding(
                    document_id=document.id, vector=embedding_vector
                )
                db.add(embedding_entry)

            await db.commit()  # Commit transaction to save document and embedding

        return {"message": "Document processed successfully"}  # Return success response

    async def process_documents_batch(self, documents: list[DocumentUploadRequest]):
        """
        Processes multiple documents concurrently using asyncio.gather.
        - Each document is processed independently in parallel.
        """
        tasks = [
            self.process_document(doc.filename, doc.content) for doc in documents
        ]  # Create tasks for each document
        return await asyncio.gather(*tasks)  # Execute all tasks concurrently
