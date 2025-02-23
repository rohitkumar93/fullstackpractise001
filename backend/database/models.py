from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from .config import Base

class Document(Base):
    """
    Stores uploaded documents. Currently raw text and ArXiv Paper formats supported
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=True)  # Make nullable for ArXiv papers
    doc_metadata = Column(ARRAY(String))
    source = Column(String, nullable=False, default="upload")  # "upload" or "arxiv"
    url = Column(String, nullable=True)  # Store URL if ArXiv paper


class Embedding(Base):
    """
    Stores vector embeddings for fast similarity search.
    """
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False)
    vector = Column(Vector(384), nullable=True)


class SelectedDocument(Base):
    """
    Stores user-selected documents to filter retrieval results.
    """
    __tablename__ = "selected_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)