from pydantic import BaseModel
from typing import List

class DocumentSelectionRequest(BaseModel):
    """
    Defines the request structure for selecting specific documents.
    """
    document_ids: List[str]

class DocumentSelectionResponse(BaseModel):
    """
    Defines the response structure listing selected documents.
    """
    selected_documents: List[str]
