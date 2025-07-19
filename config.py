#config.py
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///proposals.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'output')
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'md'}

