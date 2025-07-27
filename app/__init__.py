# app/__init__.py
import markdown
from babel import support
from flask import Flask, render_template, session, request, current_app
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_mail import Mail

# Initialize extensions (but don't tie them to an app yet)
db = SQLAlchemy()
load_dotenv()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()
mail = Mail()

def create_app():
    app = Flask(__name__)
  #  app.config.from_object('config.Config')
    app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    moment.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'auth.login'
    basedir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.join(basedir, os.pardir)
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(project_root, 'app', 'translations')
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['LANGUAGES'] = {'en': 'English', 'sw': 'Swahili'}

    def get_locale():
        if 'language' in session and session['language'] in current_app.config['LANGUAGES']:
            return session['language']

        user_lang_cookie = request.cookies.get('user_lang')
        if user_lang_cookie and user_lang_cookie in current_app.config['LANGUAGES']:
            session['language'] = user_lang_cookie
            return user_lang_cookie

        best_match = request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())
        return best_match

    babel = Babel(app, locale_selector=get_locale)

    @app.context_processor
    def inject_global_data():
        return dict(
            current_languages=app.config['LANGUAGES'],
            get_locale=get_locale # Your custom get_locale function
        )

    # Configurations
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'temp_downloads')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
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

        # Add markdown filter

    @app.template_filter('markdown')
    def markdown_filter(text):
        return markdown.markdown(text)

    @app.context_processor
    def inject_global_data():
        return dict(
            current_languages=app.config['LANGUAGES'],
            get_locale=get_locale  # Your custom get_locale function
        )

    @app.after_request
    def add_header(response):
        response.cache_control.no_store = True
        return response

    return app


