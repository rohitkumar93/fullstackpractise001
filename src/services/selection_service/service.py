from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from ...backend.database.config import SessionLocal
from ...backend.database.models import SelectedDocument
from .schemas import DocumentSelectionRequest, DocumentSelectionResponse

class DocumentSelectionService:
    """
    Manages document selection, allowing users to specify which
    documents should be used in the Q&A process.
    """

    def __init__(self):
        self.SessionLocal: sessionmaker = SessionLocal

    async def get_selected_documents(self) -> DocumentSelectionResponse:
        """
        Retrieves the list of selected documents from the database.
        """
        async with self.SessionLocal() as session:
            result = await session.execute(select(SelectedDocument.document_id))
            selected_docs = result.scalars().all()
            return DocumentSelectionResponse(selected_documents=[str(doc) for doc in selected_docs])

    async def add_selected_documents(self, request: DocumentSelectionRequest) -> dict:
        """
        Adds document IDs to the selection list.
        """
        async with self.SessionLocal() as session:
            async with session.begin():
                for doc_id in request.document_ids:
                    session.add(SelectedDocument(document_id=int(doc_id)))
            await session.commit()
        return {"message": "Documents selected successfully"}

    async def remove_selected_documents(self, request: DocumentSelectionRequest) -> dict:
        """
        Removes document IDs from the selection list.
        """
        async with self.SessionLocal() as session:
            async with session.begin():
                await session.execute(
                    delete(SelectedDocument)
                    .where(SelectedDocument.document_id.in_([int(doc) for doc in request.document_ids]))
                )
            await session.commit()
        return {"message": "Documents removed from selection"}