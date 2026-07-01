from fastapi import APIRouter, Depends
from core.database import get_database
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.curriculum import router as curriculum_router
from api.v1.endpoints.progress import router as progress_router
from api.v1.endpoints.assessments import router as assessments_router

router = APIRouter()

# Register core endpoint modules
router.include_router(auth_router, prefix="/auth")
router.include_router(curriculum_router, prefix="/curriculum")
router.include_router(progress_router, prefix="/progress")
router.include_router(assessments_router, prefix="/assessments")

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

