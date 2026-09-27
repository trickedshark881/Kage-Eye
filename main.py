# main.py

from config import (
    MAL_CLIENT_ID,
    TOPIC_ID,
    SHEET_ID,
    PASSING_THRESHOLD,
    REPORT_FILE,
    STATE_FILE
)

from mal_client import MALClient
from sheets_client import SheetsClient
from state_manager import StateManager
from report_writer import ReportWriter
from logger_setup import setup_logger


def main():

    logger = setup_logger()

    print("=" * 50)
    print("Starting Report Generation")
    print("=" * 50)

    logger.info("Report generation started")

    # Clients
    mal = MALClient(
        MAL_CLIENT_ID,
        TOPIC_ID
    )

    sheets = SheetsClient(
        SHEET_ID
    )

    state = StateManager(
        STATE_FILE
    )

    report = ReportWriter(
        REPORT_FILE
    )

    # Always create fresh Excel report
    report.create_fresh_report()

    # Retrieve qualifying MAL forum posts
    submissions = mal.get_valid_submissions()

    print(
        f"Found {len(submissions)} valid forum submissions"
    )

    logger.info(
        f"Found {len(submissions)} valid forum submissions"
    )

    passed_count = 0
    failed_count = 0
    missing_count = 0
    skipped_count = 0

    for submission in submissions:

        username = submission[
            "submitted_username"
        ]

        reply_number = submission[
            "reply_number"
        ]

        forum_user = submission[
            "forum_user"
        ]

        logger.info(
            f"Processing reply={reply_number} "
            f"user={username}"
        )

        print()
        print(
            f"Processing reply #{reply_number}"
        )
        print(
            f"Username: {username}"
        )

        # Find latest form response
        form_data = (
            sheets.find_latest_submission(
                username
            )
        )

        # =========================
        # MISSING
        # =========================

        if form_data is None:

            print("Result: MISSING")

            report.add_missing(
                username,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                "N/A",
                "Missing",
                "N/A"
            )

            missing_count += 1

            logger.warning(
                f"MISSING | user={username} "
                f"reply={reply_number}"
            )

            continue

        timestamp = form_data["timestamp"]
        score = form_data["score"]
        score_raw = form_data["score_raw"]

        # =========================
        # ALREADY PROCESSED
        # =========================

        if state.already_processed(
            username,
            timestamp
        ):

            print("Already processed. Skipping.")

            skipped_count += 1

            logger.info(
                f"SKIPPED | user={username} "
                f"timestamp={timestamp}"
            )

            continue

        # Invalid/missing score protection
        if score is None:

            print("Score could not be parsed.")

            report.add_missing(
                username,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                score_raw,
                "Missing",
                timestamp
            )

            missing_count += 1

            logger.warning(
                f"INVALID SCORE | user={username} "
                f"value={score_raw}"
            )

            continue

        # =========================
        # PASSED
        # =========================

        if score >= PASSING_THRESHOLD:

            print("Result: PASSED")

            report.add_passed(
                username,
                score_raw,
                timestamp,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                score_raw,
                "Passed",
                timestamp
            )

            passed_count += 1

            logger.info(
                f"PASSED | user={username} "
                f"score={score_raw}"
            )

        # =========================
        # FAILED
        # =========================

        else:

            print("Result: FAILED")

            report.add_failed(
                username,
                score_raw,
                timestamp,
                reply_number
            )

            report.add_audit(
                reply_number,
                forum_user,
                username,
                score_raw,
                "Failed",
                timestamp
            )

            failed_count += 1

            logger.info(
                f"FAILED | user={username} "
                f"score={score_raw}"
            )

        # Remember this exact Google Form submission
        state.mark_processed(
            username,
            timestamp
        )

    report.update_summary()

    logger.info(
        f"Completed | "
        f"Passed={passed_count} "
        f"Failed={failed_count} "
        f"Missing={missing_count} "
        f"Skipped={skipped_count}"
    )

    print()
    print("=" * 50)
    print("REPORT COMPLETED")
    print("=" * 50)

    print(f"Passed : {passed_count}")
    print(f"Failed : {failed_count}")
    print(f"Missing: {missing_count}")
    print(f"Skipped: {skipped_count}")

    print()
    print(
        f"Excel report saved to: {REPORT_FILE}"
    )


if __name__ == "__main__":
    main()
