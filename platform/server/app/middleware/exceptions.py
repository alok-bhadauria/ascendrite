import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.errors import AppException

logger = logging.getLogger(__name__)

import uuid
import time
from app.core.logging import correlation_id_var

async def exception_handler_middleware(request: Request, call_next):
    # Retrieve or generate correlation ID
    correlation_id = request.headers.get("X-Correlation-ID") or request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = correlation_id_var.set(correlation_id)
    
    start_time = time.time()
    try:
        response = await call_next(request)
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log structured request metadata
        logger.info(
            f"HTTP {request.method} {request.url.path} completed in {duration_ms}ms",
            extra={
                "route": request.url.path,
                "duration": duration_ms,
                "method": request.method,
                "status_code": response.status_code
            }
        )
        
        # Append correlation and duration headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{duration_ms}ms"
        return response
    except AppException as ex:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.warning(
            f"AppException {ex.code} in {request.url.path}: {ex.message}",
            extra={"route": request.url.path, "duration": duration_ms}
        )
        response = JSONResponse(
            status_code=ex.status_code,
            content={
                "status": "error",
                "error": {
                    "code": ex.code,
                    "message": ex.message,
                    "correlation_id": correlation_id,
                    "details": ex.details
                }
            }
        )
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{duration_ms}ms"
        return response
    except Exception as ex:
        duration_ms = int((time.time() - start_time) * 1000)
        logger.error(
            f"Unhandled Exception in request path '{request.url.path}': {ex}",
            exc_info=True,
            extra={"route": request.url.path, "duration": duration_ms}
        )
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unhandled internal server error occurred.",
                    "correlation_id": correlation_id,
                    "details": []
                }
            }
        )
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{duration_ms}ms"
        return response
    finally:
        correlation_id_var.reset(token)
