from . import db
from datetime import datetime

class ExamToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    exam_name = db.Column(db.String(200), nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

class QuizSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('exam_token.id'))
    student_name = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), nullable=False)
    student_phone = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active') # active, submitted, timeout
    fingerprint = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    score = db.Column(db.Float, default=0.0)

class ViolationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('quiz_session.id'))
    type = db.Column(db.String(50)) # tab_switch, fullscreen_exit
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(500))
