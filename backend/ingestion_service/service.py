from backend.ingestion_service.embedding_generator import EmbeddingGenerator
from backend.database.config import SessionLocal
from backend.database.models import Document, Embedding


class DocumentIngestionService:
    """
    Handles document ingestion, embedding generation, and database storage.
    """

    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()

    def process_document(self, filename: str, content: str):
        """
        Stores document text and generates embeddings for search.
        """
        db = SessionLocal()

        # Store document metadata
        document = Document(filename=filename, content=content.encode("utf-8"))
        db.add(document)
        db.commit()

        # Generate and store embeddings
        embedding_vector = self.embedding_generator.generate_embedding(content)
        embedding_entry = Embedding(document_id=document.id, vector=embedding_vector)
        db.add(embedding_entry)
        db.commit()

        db.close()
        return {"message": "Document processed successfully"}
