import time
import sys
from fastapi import APIRouter
from app.core.config import settings
from app.core.constants import APP_NAME, APP_VERSION, BUILD_VERSION, RELEASE_CHANNEL, STARTUP_TIMESTAMP
from app.core.logging import correlation_id_var

router = APIRouter()

@router.get("/metadata", tags=["System"])
async def get_system_metadata():
    """Consolidated system metadata endpoint with logically grouped runtime details"""
    return {
        "status": "success",
        "request_id": correlation_id_var.get(),
        "application": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "build": BUILD_VERSION,
            "release_channel": RELEASE_CHANNEL
        },
        "runtime": {
            "environment": settings.APP_ENV,
            "uptime_seconds": time.time() - STARTUP_TIMESTAMP,
            "startup_timestamp": STARTUP_TIMESTAMP,
            "python_version": sys.version
        }
    }