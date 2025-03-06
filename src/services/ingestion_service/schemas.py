from pydantic import BaseModel
from typing import List


# Existing Schema for Single Document
class DocumentUploadRequest(BaseModel):
    filename: str
    content: str


class DocumentUploadResponse(BaseModel):
    message: str


# ✅ New Schema for Batch Upload
class BatchUploadRequest(BaseModel):
    documents: List[DocumentUploadRequest]  # Expecting multiple documents
