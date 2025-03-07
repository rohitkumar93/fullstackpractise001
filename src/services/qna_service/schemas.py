from pydantic import BaseModel


class QueryRequest(BaseModel):
    """
    Represents a user query for the QnA service.
    """

    question: str
    top_k: int = 5  # Default to retrieving top 5 relevant documents


class QueryResponse(BaseModel):
    """
    Represents the response from the QnA service, including the retrieved answer.
    """

    answer: str
