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

    # Auto-run DB migrations on startup so the like table (and any future
    # migrations) are applied automatically on Render without needing the
    # paid Shell feature. Safe to run repeatedly — it is idempotent.
    with app.app_context():
        try:
            upgrade()
            logger.info("[BLOGIFY] flask db upgrade completed.")
        except Exception as e:  # noqa: BLE001
            logger.error("[BLOGIFY] flask db upgrade FAILED: %s", e)

    return app

