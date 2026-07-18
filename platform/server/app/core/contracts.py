from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseMetadata(BaseModel):
    timing_ms: int
    api_version: str = "v1"
    pagination: Optional[Dict[str, Any]] = None

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    request_id: str
    timestamp: float
    data: T
    meta: ResponseMetadata
    links: Dict[str, str] = {}

class ErrorDetail(BaseModel):
    code: str
    message: str
    correlation_id: str
    details: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
