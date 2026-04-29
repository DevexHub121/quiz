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
        
    return app
