import feedparser
import httpx
import asyncio
from ..ingestion_service.service import DocumentIngestionService

ARXIV_API_URL = "http://export.arxiv.org/api/query"


async def fetch_arxiv_papers(question: str, max_results: int = 5):
    """
    Fetches papers from ArXiv based on a query.
    """
    print("Fetching papers from ArXiv...")
    params = {
        "search_query": question,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    print("params used for fetching papers", params)

    async with httpx.AsyncClient() as client:
        response = await client.get(ARXIV_API_URL, params=params)
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
            "url": entry.link,
        }
        papers.append(paper_data)
        print("paper_data", paper_data)

    return papers


async def store_papers_in_db(papers):
    print("Storing papers in the database...")
    service = DocumentIngestionService()  # Initialize service

    for paper in papers:
        print("paper", paper)
        await service.process_document(
            filename=paper["title"], content=paper["abstract"]
        )


# Example usage
async def main():
    papers = await fetch_arxiv_papers(question="machine learning", max_results=5)
    await store_papers_in_db(papers)


if __name__ == "__main__":
    asyncio.run(main())
