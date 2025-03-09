from sqlalchemy.future import select  # Import select function for async queries
from sqlalchemy import delete  # Import delete function to remove records
from sqlalchemy.orm import (
    sessionmaker,
)  # Import sessionmaker for creating database sessions
from src.backend.database.config import (
    AsyncSessionLocal,
)  # Import async session factory for DB connection
from src.backend.database.models import (
    SelectedDocument,
)  # Import ORM model for selected documents
from .schemas import (
    DocumentSelectionRequest,
    DocumentSelectionResponse,
)  # Import request/response schemas


class DocumentSelectionService:
    """
    Manages document selection, allowing users to specify which
    documents should be used in the Q&A process.
    """

    def __init__(self):
        self.SessionLocal: sessionmaker = (
            AsyncSessionLocal  # Initialize async session factory
        )

    async def get_selected_documents(self) -> DocumentSelectionResponse:
        """
        Retrieves the list of selected documents from the database.
        - Executes a query to fetch selected document IDs.
        - Converts them to a response object.
        """
        async with self.SessionLocal() as session:  # Open an async database session
            result = await session.execute(
                select(SelectedDocument.document_id)
            )  # Execute query to fetch document IDs
            selected_docs = result.scalars().all()  # Extract list of document IDs
            return DocumentSelectionResponse(
                selected_documents=[
                    str(doc) for doc in selected_docs
                ]  # Convert IDs to strings for response
            )

    async def add_selected_documents(self, request: DocumentSelectionRequest) -> dict:
        """
        Adds document IDs to the selection list.
        - Inserts document IDs into the `selected_documents` table.
        - Uses a transaction that auto-commits on success.
        """
        async with self.SessionLocal() as session:  # Open async database session
            async with session.begin():  # Start transaction (auto-commits on exit)
                for doc_id in request.document_ids:
                    session.add(
                        SelectedDocument(document_id=int(doc_id))
                    )  # Add each document ID
        return {"message": "Documents selected successfully"}

    async def remove_selected_documents(
        self, request: DocumentSelectionRequest
    ) -> dict:
        """
        Removes document IDs from the selection list.
        - Deletes matching records from `selected_documents` table.
        - Uses a transaction that auto-commits on success.
        """
        async with self.SessionLocal() as session:  # Open async database session
            async with session.begin():  # Start transaction (auto-commits on exit)
                await session.execute(
                    delete(SelectedDocument).where(
                        SelectedDocument.document_id.in_(
                            [
                                int(doc) for doc in request.document_ids
                            ]  # Convert document IDs to integers for deletion
                        )
                    )
                )
        return {"message": "Documents removed from selection"}
