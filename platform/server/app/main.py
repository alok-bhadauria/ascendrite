import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.database.mongodb import connect_to_mongo, close_mongo_connection
from app.middleware.exceptions import exception_handler_middleware
from app.api.v1.router import router as v1_router

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Ascendrite API Server core resources...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down core resources...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.APP_NAME,
    description="Ascendrite Enterprise Knowledge Delivery and Interactive Learning Platform API Server",
    version="1.0.0",
    debug=settings.APP_DEBUG,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=exception_handler_middleware)

app.include_router(v1_router, prefix="/api/v1")
