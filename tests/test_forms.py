from flaskblog.posts.forms import PostForm, CommentForm
from flaskblog.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)


def test_post_form_valid(app):
    form = PostForm(title="A title", content="Some content")
    assert form.validate() is True


def test_post_form_requires_title(app):
    form = PostForm(title="", content="Some content")
    assert form.validate() is False
    assert "title" in form.errors


def test_comment_form_requires_content(app):
    form = CommentForm(content="")
    assert form.validate() is False
    assert "content" in form.errors


def test_registration_form_valid(app):
    form = RegistrationForm(
        username="newuser",
        email="new@example.com",
        password="secret",
        confirm_password="secret",
    )
    assert form.validate() is True


def test_registration_password_mismatch(app):
    form = RegistrationForm(
        username="newuser",
        email="new@example.com",
        password="secret",
        confirm_password="different",
    )
    assert form.validate() is False
    assert "confirm_password" in form.errors


def test_registration_short_username(app):
    form = RegistrationForm(
        username="a",
        email="new@example.com",
        password="secret",
        confirm_password="secret",
    )
    assert form.validate() is False
    assert "username" in form.errors


def test_registration_invalid_email(app):
    form = RegistrationForm(
        username="newuser",
        email="not-an-email",
        password="secret",
        confirm_password="secret",
    )
    assert form.validate() is False
    assert "email" in form.errors


def test_registration_duplicate_username(app, user):
    form = RegistrationForm(
        username="tester",
        email="other@example.com",
        password="secret",
        confirm_password="secret",
    )
    assert form.validate() is False
    assert "username" in form.errors


def test_registration_duplicate_email(app, user):
    form = RegistrationForm(
        username="unique",
        email="tester@example.com",
        password="secret",
        confirm_password="secret",
    )
    assert form.validate() is False
    assert "email" in form.errors


def test_login_form_valid(app):
    form = LoginForm(email="tester@example.com", password="password")
    assert form.validate() is True


def test_login_form_requires_email(app):
    form = LoginForm(email="", password="password")
    assert form.validate() is False
    assert "email" in form.errors


def test_request_reset_form_unknown_email(app):
    form = RequestResetForm(email="missing@example.com")
    assert form.validate() is False
    assert "email" in form.errors


def test_request_reset_form_known_email(app, user):
    form = RequestResetForm(email="tester@example.com")
    assert form.validate() is True


def test_reset_password_mismatch(app):
    form = ResetPasswordForm(password="secret", confirm_password="nope")
    assert form.validate() is False
    assert "confirm_password" in form.errors


def test_reset_password_valid(app):
    form = ResetPasswordForm(password="secret", confirm_password="secret")
    assert form.validate() is True


def test_update_account_form_valid_when_unchanged(app, user, client):
    # validate_username / validate_email reference current_user, so we log in first.
    from tests.conftest import login

    login(client)
    with client:
        client.get("/account")
        form = UpdateAccountForm(username="tester", email="tester@example.com")
        assert form.validate() is True
