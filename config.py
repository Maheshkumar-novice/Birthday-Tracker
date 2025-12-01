import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'birthdays.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session & Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Authentication
    APP_PASSWORD = os.environ.get('APP_PASSWORD') or 'birthday123'
