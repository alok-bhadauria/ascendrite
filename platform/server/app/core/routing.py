import json
import time
from typing import Callable, Any
from fastapi import Request, Response
from fastapi import APIRouter as FastAPIRouter
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.core.logging import correlation_id_var

class EnvelopeRoute(APIRoute):
    """Custom APIRoute class that automatically wraps 200 OK responses in SuccessResponse"""
    def get_route_handler(self) -> Callable[[Request], Any]:
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            start_time = time.time()
            response: Response = await original_route_handler(request)
            
            # Intercept standard successful JSONResponse
            if isinstance(response, JSONResponse) and response.status_code == 200:
                try:
                    data = json.loads(response.body.decode("utf-8"))
                    
                    # If it already matches SuccessResponse layout, pass it through
                    if isinstance(data, dict) and "success" in data and "request_id" in data:
                        return response
                        
                    duration_ms = int((time.time() - start_time) * 1000)
                    wrapped_content = {
                        "success": True,
                        "request_id": correlation_id_var.get() or "unknown",
                        "timestamp": time.time(),
                        "data": data,
                        "meta": {
                            "timing_ms": duration_ms,
                            "api_version": "v1"
                        },
                        "links": {}
                    }
                    headers = dict(response.headers)
                    headers.pop("content-length", None)
                    return JSONResponse(
                        content=wrapped_content,
                        status_code=200,
                        headers=headers
                    )
                except Exception:
                    return response
            return response
            
        return custom_route_handler

class APIRouter(FastAPIRouter):
    def __init__(self, *args, **kwargs):
        if "route_class" not in kwargs:
            kwargs["route_class"] = EnvelopeRoute
        super().__init__(*args, **kwargs)
