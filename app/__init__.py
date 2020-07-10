from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth_bp.login'
login.login_message = 'Please log in to access this page'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    with app.app_context():
        from .auth import auth_bp
        from .main import main_bp
        from .errors import errors_bp

        from . import models

        app.register_blueprint(errors_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        return app
