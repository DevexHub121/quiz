from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/quiz_v2.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Register Blueprints
        from .routes.auth import auth_bp
        from .routes.quiz import quiz_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(quiz_bp)
        
        # Create database tables
        from . import models
        db.create_all()

        # Seed initial token if empty
        from .models import ExamToken
        from datetime import datetime, timedelta
        if not ExamToken.query.first():
            default_token = ExamToken(
                token="QUIZ-2026-TEST",
                exam_name="General Knowledge Quiz 2026",
                expiry_time=datetime.utcnow() + timedelta(days=30),
                is_used=False
            )
            db.session.add(default_token)
            db.session.commit()
            print("Database seeded with default token.")
        
        # Route to fetch QR Code dynamically
        import qrcode
        import io
        from flask import send_file, request
        @app.route('/get_qr')
        def get_qr():
            # Get the base URL from the request
            base_url = request.host_url.rstrip('/')
            token = "QUIZ-2026-TEST"
            link = f"{base_url}/?exam_token={token}"
            
            # Generate QR
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to buffer
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            return send_file(buf, mimetype='image/png')


    return app
