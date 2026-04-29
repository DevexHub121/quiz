# Secure Proctored Quiz Platform

A robust, mobile-first web-based quiz system designed for secure examinations. Fetches questions live from Google Sheets and syncs results in real-time.

## 🚀 Key Features
- **Live Google Sheets Integration**: Fetch questions from multiple tabs and sync results instantly.
- **Proctored Mode (Anti-Cheat)**:
  - Fullscreen enforcement.
  - Tab switching & window blur detection.
  - Context menu and copy-paste disabled.
  - Prevent accidental close/refresh.
- **Mobile-First Design**: "Standalone" web app mode support for a dedicated testing window.
- **15-Minute Auto-Submission**: Synchronized server-side timer.
- **Duplicate Prevention**: Prevents students from attempting the exam more than once with the same email/phone.

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Google Sheets
- **Question Bank**: Ensure your sheet is shared as "Anyone with the link can view".
- **Result Sync**:
  1. Open your Result Google Sheet.
  2. Go to `Extensions > Apps Script` and paste the provided sync script.
  3. Deploy as a Web App and copy the URL.
  4. Update `app/excel_handler.py` with your `RESULT_SYNC_URL`.

### 3. Run Locally
```bash
python run.py
```

## 📂 Project Structure
- `app/`: Main application package.
  - `routes/`: Blueprint-based routing logic.
  - `static/`: CSS/JS/Images.
  - `templates/`: Jinja2 HTML templates.
- `data/`: Local SQLite database and record backups.
- `run.py`: Entry point for the application.

## 🌐 Deployment
This project is ready for deployment on **Render**, **Railway**, or **Heroku** using the included `Procfile` and `gunicorn`.
