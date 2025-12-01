from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # Register blueprints
    from app import routes, auth
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)
    
    with app.app_context():
        db.create_all()
    
    return app
