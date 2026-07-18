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
    logger.info("Initializing Ascendrite Platform core services...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down Platform core resources...")
    await close_mongo_connection()

app = FastAPI(
    title="Ascendrite Platform API Server",
    description="High-throughput educational platform core engine exposing curriculum delivery, user progress aggregates, assessments validation, and AI search interfaces.",
    version="1.0.0",
    terms_of_service="https://ascendrite.com/terms",
    contact={
        "name": "Ascendrite Engineering Support",
        "url": "https://ascendrite.com/support",
        "email": "engineering@ascendrite.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://ascendrite.com/license",
    },
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
