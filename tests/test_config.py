import importlib
import os

import flaskblog.config as config_module


def reload_config():
    return importlib.reload(config_module).Config


def test_default_sqlite_uri(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    cfg = reload_config()
    assert cfg.SQLALCHEMY_DATABASE_URI == "sqlite:///site.db"


def test_postgres_prefix_is_rewritten(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@host:5432/db")
    cfg = reload_config()
    assert cfg.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@host:5432/db"


def test_postgresql_url_left_untouched(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/db")
    cfg = reload_config()
    assert cfg.SQLALCHEMY_DATABASE_URI == "postgresql://user:pass@host:5432/db"


def test_secret_key_from_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "super-secret")
    cfg = reload_config()
    assert cfg.SECRET_KEY == "super-secret"


def test_secret_key_fallback(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    cfg = reload_config()
    assert cfg.SECRET_KEY == "dev-fallback-change-in-production"


def test_mail_credentials_from_env(monkeypatch):
    monkeypatch.setenv("EMAIL_USER", "mailer@example.com")
    monkeypatch.setenv("EMAIL_PASS", "mailpass")
    cfg = reload_config()
    assert cfg.MAIL_USERNAME == "mailer@example.com"
    assert cfg.MAIL_PASSWORD == "mailpass"


def test_mail_static_settings(monkeypatch):
    cfg = reload_config()
    assert cfg.MAIL_SERVER == "smtp.googlemail.com"
    assert cfg.MAIL_PORT == 587
    assert cfg.MAIL_USE_TLS is True


def teardown_module(module):
    # Restore the module to its default (env-independent) state for other tests.
    os.environ.pop("DATABASE_URL", None)
    importlib.reload(config_module)
