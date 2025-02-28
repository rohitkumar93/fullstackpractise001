import uvicorn
import logging
import os
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from backend.qna_service.routes import router as qna_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True  # ✅ Forces logging to reconfigure, fixing silent logs
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app with a descriptive project title.
# for better API documentation and future scalability.
app = FastAPI(title="RAG-based Q&A System")

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
def startup():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log incoming requests for debugging.
    """
    body = await request.body()
    logger.debug(f"📥 Incoming Request: {request.method} {request.url} - Body: {body.decode()}")

    response = await call_next(request)

    logger.debug(f"📤 Response Status: {response.status_code}")
    return response


# Ensure service routers are imported correctly
from backend.ingestion_service.routes import router as ingestion_router
from backend.retrieval_service.routes import router as retrieval_router
from backend.selection_service.routes import router as selection_router

# Segregation of API prefixes and tags for API clarity
app.include_router(ingestion_router, prefix="/ingestion", tags=["Document Ingestion"])
app.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval & Q&A"])
app.include_router(selection_router, prefix="/selection", tags=["Document Selection"])
app.include_router(qna_router, prefix="/qna", tags=["Q&A"])

# Run the application using Uvicorn with a defined host and port.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
