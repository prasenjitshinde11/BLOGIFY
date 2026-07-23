import pytest

from flaskblog import create_app, db, bcrypt
from flaskblog.config import Config
from flaskblog.models import User, Post


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"
    MAIL_SUPPRESS_SEND = True
    SERVER_NAME = "localhost"


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_user(app):
    def _make_user(username="tester", email="tester@example.com", password="password"):
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    return _make_user


@pytest.fixture
def user(make_user):
    return make_user()


@pytest.fixture
def make_post(app):
    def _make_post(author, title="Sample Title", content="Sample content"):
        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()
        return post

    return _make_post


def login(client, email="tester@example.com", password="password"):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )
