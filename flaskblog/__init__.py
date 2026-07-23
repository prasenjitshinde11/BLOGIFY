import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

logger = logging.getLogger(__name__)


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Automatically apply any pending DB migrations on startup.
    # Wrapping in try/except so a migration error doesn't crash the entire app
    # on every request — the error will be logged and visible in Render logs.
    with app.app_context():
        try:
            upgrade()
            logger.info("[BLOGIFY] flask db upgrade completed successfully.")
        except Exception as e:  # noqa: BLE001
            logger.error("[BLOGIFY] flask db upgrade FAILED: %s", e)

    return app
