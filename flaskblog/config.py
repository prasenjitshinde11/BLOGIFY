import os
from dotenv import load_dotenv

# Load variables from .env file (if present) so local dev works without
# manually exporting environment variables in every terminal session.
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-change-in-production')

    # Support DATABASE_URL from Render/Heroku; fix postgres:// prefix for SQLAlchemy
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    # ── Mail (SMTP) ──────────────────────────────────────────────────────────
    # For LOCAL DEVELOPMENT: use Mailtrap (free fake inbox at mailtrap.io)
    #   MAIL_SERVER  = sandbox.smtp.mailtrap.io
    #   MAIL_PORT    = 2525
    #   Get USERNAME & PASSWORD from: mailtrap.io → Inboxes → SMTP Settings → Flask-Mail
    #
    # For PRODUCTION: use Gmail App Password or SendGrid
    #   MAIL_SERVER  = smtp.gmail.com
    #   MAIL_PORT    = 587
    MAIL_SERVER   = os.environ.get('MAIL_SERVER',   'sandbox.smtp.mailtrap.io')
    MAIL_PORT     = int(os.environ.get('MAIL_PORT', 2525))
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS',  'True').lower() == 'true'
    MAIL_USE_SSL  = os.environ.get('MAIL_USE_SSL',  'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # Set to True to skip sending emails entirely (useful in unit tests)
    MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND', 'False').lower() == 'true'