import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-change-in-production')
    # Support DATABASE_URL from Render/Heroku; fix postgres:// prefix for SQLAlchemy
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    