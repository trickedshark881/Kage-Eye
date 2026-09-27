# config.py

import os
from dotenv import load_dotenv

load_dotenv()


# ==========================
# MAL SETTINGS
# ==========================

MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")

TOPIC_ID = int(
    os.getenv("TOPIC_ID")
)

SUBMISSION_KEYWORDS = [
    word.strip().lower()
    for word in os.getenv(
        "SUBMISSION_KEYWORDS",
        "submitted,submited,submit"
    ).split(",")
    if word.strip()
]


# ==========================
# GOOGLE SHEETS
# ==========================

SHEET_ID = os.getenv("SHEET_ID")


# ==========================
# QUIZ
# ==========================

TOTAL_QUESTIONS = int(
    os.getenv(
        "TOTAL_QUESTIONS",
        4
    )
)

PASSING_THRESHOLD = int(
    os.getenv(
        "PASSING_THRESHOLD",
        1
    )
)


# ==========================
# FILES
# ==========================

REPORT_FILE = os.getenv(
    "REPORT_FILE",
    "data/results.xlsx"
)

STATE_FILE = os.getenv(
    "STATE_FILE",
    "data/processed_state.json"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "data/monitor.log"
)


# ==========================
# REPORT
# ==========================

GENERATE_AUDIT_LOG = (
    os.getenv(
        "GENERATE_AUDIT_LOG",
        "True"
    ).lower() == "true"
)

GENERATE_SUMMARY = (
    os.getenv(
        "GENERATE_SUMMARY",
        "True"
    ).lower() == "true"
)
