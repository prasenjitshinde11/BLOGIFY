from unittest.mock import patch

from flaskblog.models import User
from tests.conftest import login


def test_register_get(client):
    resp = client.get("/register")
    assert resp.status_code == 200


def test_register_creates_user(client):
    resp = client.post(
        "/register",
        data={
            "username": "brandnew",
            "email": "brandnew@example.com",
            "password": "secret",
            "confirm_password": "secret",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert User.query.filter_by(username="brandnew").first() is not None


def test_register_redirects_authenticated_user(client, user):
    login(client)
    resp = client.get("/register")
    assert resp.status_code == 302
    assert "/home" in resp.headers["Location"] or resp.headers["Location"].endswith("/")


def test_login_success(client, user):
    resp = login(client)
    assert resp.status_code == 200


def test_login_invalid_credentials(client, user):
    resp = client.post(
        "/login",
        data={"email": "tester@example.com", "password": "wrong"},
        follow_redirects=True,
    )
    assert b"Login unsuccessful" in resp.data


def test_login_redirects_next_page(client, user):
    resp = client.post(
        "/login?next=/about",
        data={"email": "tester@example.com", "password": "password"},
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/about")


def test_login_ignores_external_next(client, user):
    resp = client.post(
        "/login?next=http://evil.com",
        data={"email": "tester@example.com", "password": "password"},
    )
    assert resp.status_code == 302
    assert "evil.com" not in resp.headers["Location"]


def test_logout(client, user):
    login(client)
    resp = client.get("/logout")
    assert resp.status_code == 302


def test_account_requires_login(client):
    resp = client.get("/account")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_account_get_logged_in(client, user):
    login(client)
    resp = client.get("/account")
    assert resp.status_code == 200


def test_account_update(client, user):
    login(client)
    resp = client.post(
        "/account",
        data={"username": "updatedname", "email": "updated@example.com"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert User.query.filter_by(username="updatedname").first() is not None


def test_user_posts_page(client, user, make_post):
    make_post(user, title="On The User Page")
    resp = client.get(f"/user/{user.username}")
    assert resp.status_code == 200
    assert b"On The User Page" in resp.data


def test_user_posts_unknown_user_404(client):
    resp = client.get("/user/nobody")
    assert resp.status_code == 404


def test_reset_request_get(client):
    resp = client.get("/reset_password")
    assert resp.status_code == 200


def test_reset_request_sends_email(client, user):
    with patch("flaskblog.users.routes.send_reset_email") as mock_send:
        resp = client.post(
            "/reset_password",
            data={"email": "tester@example.com"},
            follow_redirects=True,
        )
    assert resp.status_code == 200
    assert mock_send.called


def test_reset_token_invalid(client, user):
    resp = client.get("/reset_password/bad-token", follow_redirects=True)
    assert resp.status_code == 200
    assert b"invalid or expired" in resp.data


def test_reset_token_valid_updates_password(client, user):
    token = user.get_reset_token()
    resp = client.post(
        f"/reset_password/{token}",
        data={"password": "newpass", "confirm_password": "newpass"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # Old password should no longer authenticate.
    bad = client.post(
        "/login",
        data={"email": "tester@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert b"Login unsuccessful" in bad.data
