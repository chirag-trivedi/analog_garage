import json
import logging


class JsonFormatter(logging.Formatter):
    """Custom logging formatter to output log messages in JSON format."""

    def __init__(self, datefmt: str = "%Y-%m-%dT%H:%M:%S"):
        super().__init__(datefmt=datefmt)

    def format(self, record):
        log_message = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "line": record.lineno,
        }

        try:
            return json.dumps(log_message)
        except (TypeError, ValueError) as e:
            return f"Error formatting log message to JSON: {e}"
