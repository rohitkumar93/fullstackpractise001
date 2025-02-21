from sqlalchemy.orm import Session

from backend.database.config import SessionLocal
from backend.database.models import SelectedDocument
from backend.selection_service.schemas import DocumentSelectionRequest, DocumentSelectionResponse


class DocumentSelectionService:
    """
    Manages document selection, allowing users to specify which
    documents should be used in the Q&A process.
    """

    def __init__(self):
        self.db: Session = SessionLocal()

    def get_selected_documents(self) -> DocumentSelectionResponse:
        """
        Retrieves the list of selected documents from the database.
        """
        selected_docs = self.db.query(SelectedDocument.document_id).all()
        return DocumentSelectionResponse(selected_documents=[str(doc[0]) for doc in selected_docs])

    def add_selected_documents(self, request: DocumentSelectionRequest):
        """
        Adds document IDs to the selection list.
        """
        for doc_id in request.document_ids:
            self.db.add(SelectedDocument(document_id=int(doc_id)))
        self.db.commit()
        return {"message": "Documents selected successfully"}

    def remove_selected_documents(self, request: DocumentSelectionRequest):
        """
        Removes document IDs from the selection list.
        """
        self.db.query(SelectedDocument).filter(SelectedDocument.document_id.in_([int(doc) for doc in request.document_ids])).delete(synchronize_session=False)
        self.db.commit()
        return {"message": "Documents removed from selection"}