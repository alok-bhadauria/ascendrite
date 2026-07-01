from fastapi import APIRouter, Depends
from core.database import get_database

router = APIRouter()

@router.get("/health", tags=["System"])
async def api_health(db = Depends(get_database)):
    """Enriched V1 API Health check verifying database connection states"""
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {
        "status": "healthy",
        "api_version": "v1",
        "database": db_status
    }
