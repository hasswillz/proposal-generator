# app/__init__.py
from flask import Flask, render_template, session, request, current_app
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
import os
from dotenv import load_dotenv
from datetime import datetime

# Initialize extensions (but don't tie them to an app yet)
db = SQLAlchemy()
load_dotenv()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    moment.init_app(app)
    login_manager.login_view = 'auth.login'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['LANGUAGES'] = {'en': 'English', 'sw': 'Swahili'}

    def get_locale():
        # Priority: URL param > session > browser default
        lang = request.args.get('lang')
        if lang in app.config['LANGUAGES']:
            return lang
        return session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys()))

    babel = Babel(app, locale_selector=get_locale)

    # Make available in templates
    @app.context_processor
    def inject_vars():
        return {
            'get_locale': get_locale,
            'current_languages': app.config['LANGUAGES']
        }

    # Make function available to templates
    #app.jinja_env.globals.update(get_locale=get_locale)
    # Configurations
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'temp_downloads')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
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


    @app.after_request
    def refresh_cache(response):
        if 'language' in session:
            response.headers['Cache-Control'] = 'no-store'
        return response