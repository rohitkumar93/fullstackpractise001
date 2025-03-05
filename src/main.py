import uvicorn
import logging
import os
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from src.services.qna_service.routes import router as qna_router
from src.services.ingestion_service.routes import router as ingestion_router
from src.services.retrieval_service.routes import router as retrieval_router
from src.services.selection_service.routes import router as selection_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True  # ✅ Forces logging to reconfigure, fixing silent logs
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG-based Q&A System")

# ✅ Use async SQLAlchemy engine
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@app.on_event("startup")
async def startup():
    """Check DB connection on startup."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))  # ✅ Use `await` for async query

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

# API Routes
app.include_router(ingestion_router, prefix="/ingestion", tags=["Document Ingestion"])
app.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval & Q&A"])
app.include_router(selection_router, prefix="/selection", tags=["Document Selection"])
app.include_router(qna_router, prefix="/qna", tags=["Q&A"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
