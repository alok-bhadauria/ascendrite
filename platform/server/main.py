import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logging import setup_logging
from core.database import connect_to_mongo, close_mongo_connection
from api.v1.router import router as v1_router

# Setup logger before main app starts
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application Startup lifecycle
    logger.info("Initializing Ascendrite API Server core resources...")
    try:
        await connect_to_mongo()
    except Exception as e:
        logger.critical(f"FastAPI startup cancelled due to database failure: {e}")
        raise e
    yield
    # Application Shutdown lifecycle
    logger.info("Shutting down core resources...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.APP_NAME,
    description="Ascendrite Enterprise Knowledge Delivery and Interactive Learning Platform API Server",
    version="1.0.0",
    debug=settings.APP_DEBUG,
    lifespan=lifespan
)

# Enforce CORS policies from config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler intercepting unhandled errors (preventing stack-trace leaks)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception in request path '{request.url.path}': {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

# Root service level checks
@app.get("/", tags=["System"])
async def root():
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "status": "online"
    }

@app.get("/health", tags=["System"])
async def health():
    """Lightweight health check for edge load balancers"""
    return {"status": "healthy"}

# Include V1 Router groups
app.include_router(v1_router, prefix="/api/v1")
