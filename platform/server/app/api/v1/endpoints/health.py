import time
from fastapi import APIRouter, status, HTTPException
from app.core.config import settings
from app.core.constants import APP_NAME, APP_VERSION, STARTUP_TIMESTAMP
from app.core.logging import correlation_id_var

router = APIRouter()

def get_uptime() -> float:
    return time.time() - STARTUP_TIMESTAMP

@router.get("", tags=["System"])
async def get_health():
    """General application health check mapping dependencies states"""
    # 1. MongoDB check
    from app.infrastructure.database.mongodb import db_manager
    mongo_start = time.time()
    mongo_ok = False
    if db_manager.is_connected and db_manager.db is not None:
        try:
            await db_manager.db.command("ping")
            mongo_ok = True
        except Exception:
            mongo_ok = False
    mongo_latency = int((time.time() - mongo_start) * 1000)

    # 2. PostgreSQL check
    pg_start = time.time()
    pg_ok = True
    try:
        from app.infrastructure.database.postgres import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        pg_ok = False
    pg_latency = int((time.time() - pg_start) * 1000)

    # Redis placeholder check
    redis_ok = True
    redis_latency = 0

    # Storage placeholder check
    storage_ok = True
    storage_latency = 0

    is_healthy = mongo_ok and pg_ok
    status_str = "healthy" if is_healthy else "degraded"

    payload = {
        "status": status_str,
        "timestamp": time.time(),
        "uptime": get_uptime(),
        "version": APP_VERSION,
        "environment": settings.APP_ENV,
        "request_id": correlation_id_var.get(),
        "dependencies": {
            "postgres": {
                "status": "connected" if pg_ok else "disconnected",
                "latency_ms": pg_latency
            },
            "mongodb": {
                "status": "connected" if mongo_ok else "disconnected",
                "latency_ms": mongo_latency
            },
            "redis": {
                "status": "connected" if redis_ok else "disconnected",
                "latency_ms": redis_latency
            },
            "storage": {
                "status": "connected" if storage_ok else "disconnected",
                "latency_ms": storage_latency
            }
        }
    }

    if not is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=payload
        )

    return payload

@router.get("/liveness", tags=["System"])
async def get_liveness():
    """Lightweight process liveness validation (zero DB queries)"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": get_uptime(),
        "version": APP_VERSION,
        "environment": settings.APP_ENV,
        "request_id": correlation_id_var.get()
    }

@router.get("/readiness", tags=["System"])
async def get_readiness():
    """Dependency readiness validations for K8s orchestration checks"""
    # PostgreSQL lightweight check
    pg_ok = True
    try:
        from app.infrastructure.database.postgres import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        pg_ok = False

    # MongoDB lightweight check
    from app.infrastructure.database.mongodb import db_manager
    mongo_ok = False
    if db_manager.is_connected and db_manager.db is not None:
        try:
            await db_manager.db.command("ping")
            mongo_ok = True
        except Exception:
            mongo_ok = False

    if not pg_ok or not mongo_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "dependencies": {
                    "postgres": "ready" if pg_ok else "offline",
                    "mongodb": "ready" if mongo_ok else "offline"
                }
            }
        )

    return {
        "status": "ready",
        "timestamp": time.time(),
        "request_id": correlation_id_var.get()
    }
