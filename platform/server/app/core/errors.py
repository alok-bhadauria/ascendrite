from typing import Any, List, Optional
from fastapi import status

class ErrorCategory:
    VALIDATION = "VALIDATION"
    AUTHENTICATION = "AUTH"
    AUTHORIZATION = "AUTH"
    BUSINESS_RULE = "RULE"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    INFRASTRUCTURE = "INFRA"
    EXTERNAL_SERVICE = "EXT"
    INTERNAL_SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"

class AppException(Exception):
    def __init__(self, message: str, code: str = "SYSTEM_INTERNAL_ERROR", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Optional[List[Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []

class EntityNotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[List[Any]] = None):
        super().__init__(message, code="NOT_FOUND_RESOURCE", status_code=status.HTTP_404_NOT_FOUND, details=details)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized session context", details: Optional[List[Any]] = None):
        super().__init__(message, code="AUTH_UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED, details=details)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden", details: Optional[List[Any]] = None):
        super().__init__(message, code="AUTH_FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN, details=details)
