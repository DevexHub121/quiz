from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..models import ExamToken, QuizSession, db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    prefilled_token = request.args.get('exam_token')
    return render_template('index.html', prefilled_token=prefilled_token)

@auth_bp.route('/validate', methods=['POST'])
def validate():
    token_str = request.form.get('token')
    name = request.form.get('name')
    email = request.form.get('email').strip().lower()
    phone = request.form.get('phone').strip()
    
    # 1. Check Token Validity
    token = ExamToken.query.filter_by(token=token_str).first()
    if not token:
        flash("Invalid Exam Token")
        return redirect(url_for('auth.index'))
    
    if token.expiry_time < datetime.utcnow():
        flash("Exam Token has expired")
        return redirect(url_for('auth.index'))

    # 2. Prevent Duplicate Attempts
    # Check if a 'submitted' session already exists for this email OR phone
    existing_session = QuizSession.query.filter(
        ((QuizSession.student_email == email) | (QuizSession.student_phone == phone)),
        (QuizSession.status == 'submitted')
    ).first()

    if existing_session:
        flash("You have already submitted this exam. Multiple attempts are not allowed.")
        return redirect(url_for('auth.index'))
    
    # 3. Create new session
    new_session = QuizSession(
        token_id=token.id,
        student_name=name,
        student_email=email,
        student_phone=phone,
        start_time=datetime.utcnow(),
        ip_address=request.remote_addr,
        status='active'
    )
    db.session.add(new_session)
    db.session.commit()
    
    session['quiz_session_id'] = new_session.id
    # Clear old quiz questions to force fresh load from Google Sheets
    session.pop('questions', None)
    
    return redirect(url_for('quiz.start'))
