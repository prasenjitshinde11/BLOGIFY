def test_404_handler(client):
    resp = client.get("/this-route-does-not-exist")
    assert resp.status_code == 404


def test_403_handler(client, make_user, make_post):
    from tests.conftest import login

    author = make_user(username="owner", email="owner@example.com")
    make_user(username="other", email="other@example.com")
    post = make_post(author)
    login(client, email="other@example.com")
    # Non-author update triggers abort(403), rendered by the error handler.
    resp = client.post(
        f"/post/{post.id}/update",
        data={"title": "x", "content": "y"},
    )
    assert resp.status_code == 403


def test_500_handler_registered(app):
    # The 500 handler is registered as an app-level error handler.
    handlers = app.error_handler_spec[None].get(500)
    assert handlers is not None
