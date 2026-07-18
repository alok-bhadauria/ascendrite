import logging
import sys
import json
from datetime import datetime, timezone
from app.core.config import settings

import contextvars

# Context local request correlation tracker
correlation_id_var = contextvars.ContextVar("correlation_id", default=None)

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "request_id": correlation_id_var.get(),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        # Inject timing metadata if present via extra attributes
        if hasattr(record, "duration"):
            log_data["duration_ms"] = record.duration
        if hasattr(record, "route"):
            log_data["route"] = record.route
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logging():
    log_level = getattr(logging, settings.APP_LOG_LEVEL.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clean existing handlers to prevent duplicate logging
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_FORMAT.lower() == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        ))

    root_logger.addHandler(handler)
    
    # Set levels for third party verbose libraries
    logging.getLogger("uvicorn.access").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
