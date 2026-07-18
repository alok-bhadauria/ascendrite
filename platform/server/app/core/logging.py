import logging
import sys
import json
import contextvars
from pathlib import Path
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from app.core.config import settings

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

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_FORMAT.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Centralized Rotating File Handlers under logs/backend/
    try:
        workspace_root = Path(__file__).resolve().parents[4]
        logs_dir = workspace_root / "logs" / "backend"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Main log file (INFO and above)
        main_file_handler = RotatingFileHandler(
            logs_dir / "backend.log",
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        main_file_handler.setLevel(log_level)
        main_file_handler.setFormatter(formatter)
        root_logger.addHandler(main_file_handler)

        # 2. Error log file (ERROR and above)
        error_file_handler = RotatingFileHandler(
            logs_dir / "error.log",
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        root_logger.addHandler(error_file_handler)
        
        print(f"File loggers successfully bound to: {logs_dir}")
    except Exception as e:
        print(f"WARNING: Centralized file loggers could not be configured: {e}", file=sys.stderr)

    logging.getLogger("uvicorn.access").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
