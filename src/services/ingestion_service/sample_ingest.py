from backend.database.config import SessionLocal
from backend.database.models import Document, Embedding, SelectedDocument
from backend.ingestion_service.embedding_generator import EmbeddingGenerator
import numpy as np

def ingest_sample_documents():
    db = SessionLocal()
    embedding_generator = EmbeddingGenerator()

    sample_docs = [
        # AI-related documents
        {"filename": "ai_intro.txt", "content": "Artificial Intelligence is transforming industries."},
        {"filename": "ml_basics.pdf", "content": "Machine Learning is a subset of AI that learns from data."},
        {"filename": "deep_learning.txt", "content": "Deep learning uses neural networks for complex tasks."},

        # Non-AI documents for ranking validation
        {"filename": "sports_news.txt", "content": "The football team won the championship after a tough season."},
        {"filename": "cooking_guide.pdf", "content": "Learn how to cook delicious meals with simple ingredients."}
    ]

    for doc in sample_docs:
        # Store document
        document = Document(filename=doc["filename"], content=doc["content"].encode("utf-8"))
        db.add(document)
        db.commit()

        # Generate and validate embedding
        embedding_vector = embedding_generator.generate_embedding(doc["content"])
        embedding_vector = np.array(embedding_vector, dtype=np.float32)  # ✅ Ensure float32 type
        assert embedding_vector.shape[0] == 384, f"❌ Vector size mismatch! Got {embedding_vector.shape[0]} instead of 384."

        # Store embedding
        embedding_entry = Embedding(document_id=document.id, vector=embedding_vector.tolist())
        db.add(embedding_entry)
        db.commit()

        # ✅ Select document for retrieval
        selected_doc = SelectedDocument(document_id=document.id)
        db.add(selected_doc)
        db.commit()

        print(f"✅ Added & Selected Document: {document.filename} | ID: {document.id} | Vector Size: {len(embedding_vector)}")

    db.close()
    print("✅ Sample documents have been added and selected for retrieval!")

if __name__ == "__main__":
    ingest_sample_documents()
