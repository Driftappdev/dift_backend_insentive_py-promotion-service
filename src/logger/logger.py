import logging
from logging.handlers import RotatingFileHandler
from src.config.config import settings

# -------------------------
# Logger configuration
# -------------------------
logger = logging.getLogger("promotion_service")
logger.setLevel(settings.log_level.upper() if hasattr(settings, "log_level") else "INFO")

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

# Stream handler (console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Optional: File handler with rotation
file_handler = RotatingFileHandler("logs/promotion_service.log", maxBytes=5*1024*1024, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Promotion service logger initialized")
