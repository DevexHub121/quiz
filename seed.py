import pandas as pd
import os
from app import create_app, db
from app.models import ExamToken
from datetime import datetime, timedelta

def create_multi_sheet_bank():
    BANK_FILE = 'data/bank.xlsx'
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # Create 4 sheets (sections)
    with pd.ExcelWriter(BANK_FILE) as writer:
        sections = ['General Knowledge', 'Mathematics', 'Reasoning', 'English']
        for section in sections:
            data = {
                'question': [f'Sample Question from {section} {i+1}?' for i in range(10)],
                'option1': ['Option A'] * 10,
                'option2': ['Option B'] * 10,
                'option3': ['Option C'] * 10,
                'option4': ['Option D'] * 10,
                'correct_option': [1] * 10
            }
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=section, index=False)
    print(f"Sample multi-sheet bank created at {BANK_FILE}")

app = create_app()

with app.app_context():
    create_multi_sheet_bank()
    
    # Create a test token
    test_token = "QUIZ-2026-TEST"
    existing = ExamToken.query.filter_by(token=test_token).first()
    
    if not existing:
        token = ExamToken(
            token=test_token,
            exam_name="Multi-Section Exam",
            expiry_time=datetime.utcnow() + timedelta(days=7)
        )
        db.session.add(token)
        db.session.commit()
        print(f"Token created: {test_token}")

print("Seeding complete.")
