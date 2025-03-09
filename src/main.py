import uvicorn  # Import ASGI server to run FastAPI
import logging  # Import logging for debugging and monitoring
from fastapi import FastAPI, Request  # Import FastAPI core and request handling
from sqlalchemy.ext.asyncio import create_async_engine  # Import async SQLAlchemy engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # Import async session for DB interactions
from sqlalchemy.orm import (
    sessionmaker,
)  # Import sessionmaker to manage database sessions
from sqlalchemy.sql import text  # Import text function to execute raw SQL queries
from src.config import DATABASE_URL  # Import database connection URL from config

# Import API route modules
from src.services.qna_service.routes import router as qna_router
from src.services.ingestion_service.routes import router as ingestion_router
from src.services.retrieval_service.routes import router as retrieval_router
from src.services.selection_service.routes import router as selection_router

# ✅ Configure application-wide logging
logging.basicConfig(
    level=logging.DEBUG,  # Set log level to DEBUG for detailed output
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log format
    force=True,  # ✅ Forces logging to reconfigure, fixing silent logs
)
logger = logging.getLogger(__name__)  # Create logger instance for this module

# ✅ Initialize FastAPI application
app = FastAPI(title="RAG-based Q&A System")  # Set API title for documentation

# ✅ Create async database engine
engine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)  # Enable SQL logging for debugging

# ✅ Define async session factory for database transactions
SessionLocal = sessionmaker(
    autocommit=False,  # Disable auto-commit (transactions must be explicitly committed)
    autoflush=False,  # Disable auto-flush (prevents unwanted DB commits)
    bind=engine,  # Bind session to the database engine
    class_=AsyncSession,  # Use asynchronous session class
)

# TODO: Cleanup I believe this event is now deprecated 
@app.on_event("startup")
async def startup():
    """✅ Ensure database connection is working when the app starts."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))  # ✅ Simple query to check DB health


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    ✅ Middleware to log incoming HTTP requests and responses.
    Useful for debugging API interactions.
    """
    body = await request.body()  # Read request body
    logger.debug(
        f"📥 Incoming Request: {request.method} {request.url} - Body: {body.decode()}"
    )

    response = await call_next(request)  # Process the request

    logger.debug(f"📤 Response Status: {response.status_code}")  # Log response status
    return response


# ✅ Register API routers for modular endpoints
app.include_router(ingestion_router, prefix="/ingestion", tags=["Document Ingestion"])
app.include_router(retrieval_router, prefix="/retrieval", tags=["Retrieval & Q&A"])
app.include_router(selection_router, prefix="/selection", tags=["Document Selection"])
app.include_router(qna_router, prefix="/qna", tags=["Q&A"])

# ✅ Start FastAPI app with Uvicorn when the script is run directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run API server on port 8000
