import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logging import setup_logging
from core.database import connect_to_mongo, close_mongo_connection, db_manager
from api.v1.router import router as v1_router

# Setup logger before main app starts
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────
    logger.info("Initializing Ascendrite API Server core resources...")
    connected = await connect_to_mongo()
    if not connected:
        logger.warning(
            "Server is starting in DEGRADED MODE — MongoDB unavailable. "
            "API endpoints requiring a database will return HTTP 503. "
            "Fix: whitelist your IP in MongoDB Atlas → Network Access."
        )
    yield
    # ── Shutdown ─────────────────────────────────────────────────────────
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
    """Health check — reports server and database connectivity state."""
    db_ok = db_manager.is_connected
    return {
        "status": "healthy" if db_ok else "degraded",
        "server": "online",
        "database": "connected" if db_ok else "unavailable — whitelist your IP in MongoDB Atlas Network Access",
    }

# Include V1 Router groups
app.include_router(v1_router, prefix="/api/v1")
