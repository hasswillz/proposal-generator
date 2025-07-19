# # app/auth/__init__.py
from flask import Blueprint
from flask_login import LoginManager

# Create the blueprint instance
auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()

# Import routes AFTER creating the blueprint to avoid circular imports
from app.auth import routes
