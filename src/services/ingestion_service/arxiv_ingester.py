import feedparser
import requests

from ..ingestion_service.service import DocumentIngestionService

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(query: str, max_results: int = 5):
    """
    Fetches papers from ArXiv based on a query.
    """
    print("Fetching papers from ArXiv...")
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    response = requests.get(ARXIV_API_URL, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from ArXiv")

    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        paper_data = {
            "title": entry.title,
            "authors": ", ".join([author.name for author in entry.authors]),
            "abstract": entry.summary,
            "published_date": entry.published,
            "url": entry.link
        }
        papers.append(paper_data)
        print("paper_data",paper_data)

    return papers


def store_papers_in_db(papers):
    print("Fetching papers from ArXiv...")
    service = DocumentIngestionService()  # Initialize service

    for paper in papers:
        print('paper',paper)
        service.process_document(filename=paper["title"], content=paper["abstract"])
