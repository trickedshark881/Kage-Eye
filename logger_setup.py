# logger_setup.py

import logging
import os

from config import LOG_FILE


def setup_logger():

    log_directory = os.path.dirname(
        LOG_FILE
    )

    if log_directory:
        os.makedirs(
            log_directory,
            exist_ok=True
        )

    logger = logging.getLogger(
        "MALFormMonitor"
    )

    logger.setLevel(
        logging.INFO
    )

    # Avoid duplicate log entries
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    return logger
