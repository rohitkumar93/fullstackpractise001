import uvicorn
import logging
from fastapi import FastAPI, Request

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True  # ✅ Forces logging to reconfigure, fixing silent logs
)
logger = logging.getLogger(__name__)


# Initialize the FastAPI appl with a descriptive project title.
# for better API documentation and future scalability.
app = FastAPI(title="RAG-based Q&A System")


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

# Run the application using Uvicorn with a defined host and port.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
