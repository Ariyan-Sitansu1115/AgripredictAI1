"""
Centralized logging configuration for AgriPredictAI.

Creates module-specific loggers with both file and console handlers.
Log files are written to the ``logs/`` directory at the project root.
"""
import logging
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Log directory (project_root/logs/)
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = _PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """
    Create (or return an existing) logger with:
      * A file handler writing DEBUG+ logs to ``logs/<name>.log``.
      * A console (stderr) handler writing ERROR+ logs.

    Calling this function multiple times with the same *name* is safe –
    handlers are added only once.
    """
    logger = logging.getLogger(name)

    # Only configure if no handlers have been attached yet
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler – all levels
    log_file = LOG_DIR / f"{name}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler – errors only (keeps stdout clean in production)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Prevent log records from propagating to the root logger
    logger.propagate = False

    return logger


# ---------------------------------------------------------------------------
# Module-specific loggers – import these directly in other modules
# ---------------------------------------------------------------------------
chatbot_logger = setup_logger("chatbot")
translator_logger = setup_logger("translator")
intent_logger = setup_logger("intent_engine")
comparison_logger = setup_logger("comparison_engine")
risk_logger = setup_logger("risk_analyzer")
stt_logger = setup_logger("speech_to_text")
tts_logger = setup_logger("text_to_speech")
lang_detect_logger = setup_logger("language_detector")
api_logger = setup_logger("api")
