import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from app.core.config import settings

if settings.logs_path is not None:
    logs_dir = Path(settings.logs_path)
    logs_dir.mkdir(parents=True, exist_ok=True)

    LOG_FILE = logs_dir / "upload_service.log"

logger = logging.getLogger("upload_service_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(getattr(logging, settings.console_log_level.upper(), logging.INFO))
ch.setFormatter(formatter)

if settings.logs_path is not None:
    fh = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=3,
        encoding="utf-8"
    )
    fh.setLevel(getattr(logging, settings.file_log_level.upper(), logging.DEBUG))
    fh.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(ch)
    if settings.logs_path is not None:
        logger.addHandler(fh)
