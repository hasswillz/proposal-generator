# app/__init__.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
import os
from datetime import datetime

# Initialize extensions (but don't tie them to an app yet)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()


def create_app():
    app = Flask(__name__)
    moment.init_app(app)
    login_manager.login_view = 'auth.login'
    # Configurations
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'temp_downloads')

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)


    # Register blueprints
    from app.auth import auth_bp
    from app.main import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    return app