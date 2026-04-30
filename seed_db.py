from app import create_app, db
from app.models import ExamToken
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    # Check if token already exists
    if not ExamToken.query.filter_by(token="QUIZ-2026-TEST").first():
        token = ExamToken(
            token="QUIZ-2026-TEST",
            exam_name="General Knowledge Quiz 2026",
            expiry_time=datetime.utcnow() + timedelta(days=30),
            is_used=False
        )
        db.session.add(token)
        db.session.commit()
        print("Successfully added token: QUIZ-2026-TEST")
    else:
        print("Token QUIZ-2026-TEST already exists.")
