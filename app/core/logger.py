"""Application logging helpers."""

from __future__ import annotations

import logging
import queue
from logging.handlers import QueueHandler, QueueListener

_LOG_QUEUE: queue.Queue[logging.LogRecord] | None = None
_LISTENER: QueueListener | None = None
_CONFIGURED = False


def configure_logger(debug: bool) -> logging.Logger:
    """Configure non-blocking console logging once."""
    global _LOG_QUEUE, _LISTENER, _CONFIGURED

    root_logger = logging.getLogger()
    level = logging.DEBUG if debug else logging.INFO
    root_logger.setLevel(level)

    if _CONFIGURED:
        return logging.getLogger("app")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter("[%(asctime)s] (%(filename)s): %(message)s", "%Y-%m-%d %H:%M:%S")
    )

    _LOG_QUEUE = queue.Queue(-1)
    queue_handler = QueueHandler(_LOG_QUEUE)
    root_logger.handlers.clear()
    root_logger.addHandler(queue_handler)

    _LISTENER = QueueListener(_LOG_QUEUE, console_handler, respect_handler_level=True)
    _LISTENER.start()
    _CONFIGURED = True

    return logging.getLogger("app")


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger for the given module name."""
    return logging.getLogger(name or "app")
