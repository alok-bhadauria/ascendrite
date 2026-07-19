from fastapi import APIRouter
from app.core.routing import EnvelopeRoute
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.curriculum import router as curriculum_router
from app.api.v1.endpoints.progress import router as progress_router
from app.api.v1.endpoints.assessments import router as assessments_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.system import router as system_router
from app.api.v1.endpoints.academic import router as academic_router
from app.api.v1.endpoints.content import router as content_router
from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.session import router as learning_router
from app.api.v1.endpoints.experience import router as experience_router
from app.api.v1.endpoints.insights import router as insights_router

router = APIRouter(route_class=EnvelopeRoute)

router.include_router(auth_router, prefix="/auth")
router.include_router(curriculum_router, prefix="/curriculum")
router.include_router(progress_router, prefix="/progress")
router.include_router(assessments_router, prefix="/assessments")
router.include_router(health_router, prefix="/health")
router.include_router(system_router, prefix="/system")
router.include_router(academic_router, prefix="/academic")
router.include_router(content_router, prefix="/knowledge-content")
router.include_router(search_router, prefix="/search")
router.include_router(learning_router, prefix="/learning")
router.include_router(experience_router, prefix="/learning/experiences")
router.include_router(insights_router, prefix="/learning/insights")
