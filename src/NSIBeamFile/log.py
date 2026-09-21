import logging
import sys
from datetime import datetime


# =============================================================================
# Logging Configuration
# =============================================================================

class ColorFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: "\033[38;5;208m", # Orange
        logging.INFO: "\033[36m",        # Cyan
        logging.WARNING: "\033[33m",     # Yellow
        logging.ERROR: "\033[31m",       # Red
        logging.CRITICAL: "\033[31m",    # Red
    }

    LEVEL_NAMES = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARN",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "ERROR",
    }

    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        level = self.LEVEL_NAMES.get(record.levelno, record.levelname)

        # Here print timestamp in gray
        timestamp = f"\033[90m{datetime.now().astimezone().isoformat(timespec='milliseconds')}\033[0m"

        return (
            f"{color}[{level}]{self.RESET} "
            f"{timestamp} "
            f"{record.getMessage()}"
        )


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)