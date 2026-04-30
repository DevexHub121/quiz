from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from ..models import QuizSession, ViolationLog, db
from ..excel_handler import load_random_questions, save_record
from datetime import datetime, timedelta
import random

quiz_bp = Blueprint('quiz', __name__)

def get_ist_time():
    """Get current time in IST (UTC+5:30)"""
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

@quiz_bp.route('/start')
def start():
    session_id = session.get('quiz_session_id')
    if not session_id:
        return redirect(url_for('auth.index'))
    
    quiz_session = QuizSession.query.get(session_id)
    if quiz_session.status != 'active':
        return redirect(url_for('auth.index'))
    
    if 'questions' not in session:
        questions = load_random_questions(questions_per_sheet=5)
        random.shuffle(questions)
        session['questions'] = questions
    else:
        questions = session['questions']
    
    return render_template('quiz.html', questions=questions, session=quiz_session)

@quiz_bp.route('/submit', methods=['POST'])
def submit():
    session_id = session.get('quiz_session_id')
    if not session_id:
        return jsonify({'success': False, 'message': 'No active session'})
    
    quiz_session = QuizSession.query.get(session_id)
    if not quiz_session or quiz_session.status != 'active':
        return redirect(url_for('auth.index'))
        
    answers = request.form.to_dict()
    questions = session.get('questions', [])
    
    # Track section-wise scores
    section_scores = {
        'Quantitative Aptitude': 0,
        'Verbal (English)': 0,
        'Reasoning': 0,
        'Programming': 0
    }
    
    total_score = 0
    for i, q in enumerate(questions):
        correct = str(q['correct_option'])
        submitted = answers.get(f'q_{i}')
        if submitted == correct:
            total_score += 1
            section = q.get('section')
            if section in section_scores:
                section_scores[section] += 1
    
    quiz_session.score = total_score
    quiz_session.status = 'submitted'
    quiz_session.end_time = datetime.utcnow()
    db.session.commit()
    
    # Format time taken
    seconds_taken = (quiz_session.end_time - quiz_session.start_time).seconds
    minutes = seconds_taken // 60
    seconds = seconds_taken % 60
    time_str = f"{minutes}m {seconds}s"
    
    # Get current submission time in IST
    submission_time_ist = get_ist_time().strftime('%Y-%m-%d %I:%M:%S %p')
    
    # Create record
    record = {
        'Name': quiz_session.student_name,
        'Phone Number': quiz_session.student_phone,
        'Gmail': quiz_session.student_email,
        'Aptitude Score': section_scores['Quantitative Aptitude'],
        'Verbal Score': section_scores['Verbal (English)'],
        'Reasoning Score': section_scores['Reasoning'],
        'Programming Score': section_scores['Programming'],
        'Total Score': total_score,
        'Time Taken': time_str,
        'Submitted At': submission_time_ist
    }
    save_record(record)
    
    answered_count = sum(1 for i in range(len(questions)) if answers.get(f'q_{i}'))
    
    return render_template('result.html', answered=answered_count, total=len(questions))

@quiz_bp.route('/log_violation', methods=['POST'])
def log_violation():
    session_id = session.get('quiz_session_id')
    if not session_id:
        return jsonify({'success': False})
    
    data = request.json
    violation = ViolationLog(
        session_id=session_id,
        type=data.get('type'),
        details=data.get('details')
    )
    db.session.add(violation)
    db.session.commit()
    
    return jsonify({'success': True})
