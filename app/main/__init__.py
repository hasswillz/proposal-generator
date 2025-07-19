# app/main/__init__.py
from flask import Blueprint

# Create blueprint instance
main_bp = Blueprint('main', __name__)
# Import routes AFTER blueprint creation to avoid circular imports
from app.main import routes