# Need to refactor this code entirely; commenting for now

# import pytest
# from unittest.mock import patch, MagicMock
# from src.services.retrieval_service.bm25_retrieval import BM25RetrievalService


# @pytest.fixture
# def bm25_service():
#     """Fixture to initialize BM25RetrievalService with mocked data."""
#     with patch(
#         "src.services.retrieval_service.bm25_retrieval.AsyncSessionLocal"
#     ) as mock_db:
#         # Mock the database session and query results
#         mock_session = MagicMock()
#         mock_db.return_value = mock_session

#         # Mock selected document IDs
#         mock_selected_ids = [1, 2, 3]
#         mock_session.query.return_value.all.return_value = [
#             (id,) for id in mock_selected_ids
#         ]

#         # Mock documents
#         mock_docs = [
#             MagicMock(id=1, content=b"Python is a programming language."),
#             MagicMock(id=2, content=b"Machine learning is a subset of AI."),
#             MagicMock(id=3, content=b"Deep learning uses neural networks."),
#         ]
#         mock_session.query.return_value.filter.return_value.all.return_value = mock_docs

#         service = BM25RetrievalService()
#         service.load_documents()
#         return service


# def test_load_documents(bm25_service):
#     """Test loading and tokenizing documents from the database."""
#     assert len(bm25_service.documents) == 3
#     assert len(bm25_service.doc_ids) == 3
#     assert bm25_service.bm25 is not None


# def test_retrieve_relevant_docs(bm25_service):
#     """Test retrieving relevant documents using BM25."""
#     query = "What is Python?"
#     top_k = 2
#     result = bm25_service.retrieve_relevant_docs(query, top_k)
#     assert len(result) == top_k
#     assert result == [1, 2]  # Assuming the first two documents are most relevant


# def test_retrieve_relevant_docs_no_documents():
#     """Test retrieving relevant documents when no documents are loaded."""
#     with patch(
#         "src.services.retrieval_service.bm25_retrieval.AsyncSessionLocal"
#     ) as mock_db:
#         mock_session = MagicMock()
#         mock_db.return_value = mock_session

#         # Mock no selected document IDs
#         mock_session.query.return_value.all.return_value = []

#         service = BM25RetrievalService()
#         service.load_documents()

#         query = "What is Python?"
#         top_k = 2
#         result = service.retrieve_relevant_docs(query, top_k)
#         assert len(result) == 0
#         assert result == []


# def test_retrieve_relevant_docs_empty_query(bm25_service):
#     """Test retrieving relevant documents with an empty query."""
#     query = ""
#     top_k = 2
#     result = bm25_service.retrieve_relevant_docs(query, top_k)
#     assert len(result) == 0
#     assert result == []


# def test_retrieve_relevant_docs_no_bm25_model():
#     """Test retrieving relevant documents when BM25 model is not initialized."""
#     with patch(
#         "src.services.retrieval_service.bm25_retrieval.AsyncSessionLocal"
#     ) as mock_db:
#         mock_session = MagicMock()
#         mock_db.return_value = mock_session

#         # Mock selected document IDs
#         mock_selected_ids = [1, 2, 3]
#         mock_session.query.return_value.all.return_value = [
#             (id,) for id in mock_selected_ids
#         ]

#         # Mock documents
#         mock_docs = [
#             MagicMock(id=1, content=b"Python is a programming language."),
#             MagicMock(id=2, content=b"Machine learning is a subset of AI."),
#             MagicMock(id=3, content=b"Deep learning uses neural networks."),
#         ]
#         mock_session.query.return_value.filter.return_value.all.return_value = mock_docs

#         service = BM25RetrievalService()
#         service.documents = []  # Clear documents to simulate no BM25 model
#         service.doc_ids = []
#         service.bm25 = None

#         query = "What is Python?"
#         top_k = 2
#         result = service.retrieve_relevant_docs(query, top_k)
#         assert len(result) == 0
#         assert result == []
