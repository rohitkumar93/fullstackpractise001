from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    """
    Defines the request payload for document uploads.
    """
    filename: str
    content: bytes  # TODO: Change to file upload mechanism if needed

class DocumentUploadResponse(BaseModel):
    """
    Defines the response structure after a document is processed.
    """
    message: str
