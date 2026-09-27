# MAL Form Monitor

A lightweight Python system that monitors a MyAnimeList forum topic, detects submission posts, matches users with their latest Google Form response, evaluates their score, and generates an Excel report.

## ✨ How It Works

```text
MyAnimeList Forum
        ↓
     MAL API
        ↓
Submission Keyword Detection
        ↓
Forum Username Extraction
        ↓
Google Sheets
        ↓
Latest Form Submission
        ↓
Score Evaluation
        ↓
Passed / Failed / Missing
        ↓
Excel Report + Audit Log
```

## 🚀 Features

- MyAnimeList Forum API integration
- Automatic forum pagination
- Case-insensitive submission keyword detection
- Automatically uses the MAL forum user's username
- Google Sheets CSV retrieval
- Latest form submission selected by timestamp
- Score parsing and pass/fail evaluation
- Missing-user detection
- Duplicate processing prevention
- Fresh Excel report on every run
- Summary and Audit Log sheets
- File logging

## 📝 Custom Submission Keywords

Submission words can be customized through `.env`:

```env
SUBMISSION_KEYWORDS=submitted,submited,submit
```

For example:

```env
SUBMISSION_KEYWORDS=submitted,submit,done
```

The system checks for these words as independent words, so responders do not need to follow a fixed message format.

Example:

```text
Submitted!

Thanks for participating.
```

The system ignores the rest of the message and identifies the MAL account that posted it.

## 📁 Project Structure

```text
mal-form-monitor/
│
├── main.py
├── config.py
├── mal_client.py
├── sheets_client.py
├── state_manager.py
├── report_writer.py
├── logger_setup.py
├── requirements.txt
├── .env
│
└── data/
    ├── results.xlsx
    ├── processed_state.json
    └── monitor.log
```

## ⚙️ Configuration

The `.env` file contains the MAL client ID, forum topic ID, Google Sheet ID, quiz settings, output paths, and report settings.

Keep `.env` private and do not commit sensitive credentials.

## ▶️ Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

The generated report is saved to:

```text
data/results.xlsx
```

## 🔄 Processing Logic

For each detected submission, the system:

1. Gets the MAL forum username.
2. Searches Google Sheets for that username.
3. Selects the latest matching form submission.
4. Parses the score.
5. Checks the passing threshold.
6. Records the result in Excel.
7. Tracks the processed form submission to prevent duplicate processing.

