from fastapi import APIRouter
from app.core.routing import EnvelopeRoute
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.curriculum import router as curriculum_router
from app.api.v1.endpoints.progress import router as progress_router
from app.api.v1.endpoints.assessments import router as assessments_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.system import router as system_router

router = APIRouter(route_class=EnvelopeRoute)

router.include_router(auth_router, prefix="/auth")
router.include_router(curriculum_router, prefix="/curriculum")
router.include_router(progress_router, prefix="/progress")
router.include_router(assessments_router, prefix="/assessments")
router.include_router(health_router, prefix="/health")
router.include_router(system_router, prefix="/system")
