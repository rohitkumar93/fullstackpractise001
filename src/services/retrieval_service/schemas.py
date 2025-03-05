from pydantic import BaseModel

class QueryRequest(BaseModel):
    """
    Defines the request structure for querying the retrieval system.
    """
    question: str

class QueryResponse(BaseModel):
    """
    Defines the response structure for generated answers.
    """
    answer: str
