from flaskblog.models import Post, Comment
from tests.conftest import login


def test_new_post_requires_login(client):
    resp = client.get("/post/new")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_new_post_get(client, user):
    login(client)
    resp = client.get("/post/new")
    assert resp.status_code == 200


def test_new_post_creates_post(client, user):
    login(client)
    resp = client.post(
        "/post/new",
        data={"title": "Fresh Post", "content": "Body text"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert Post.query.filter_by(title="Fresh Post").first() is not None


def test_view_post(client, user, make_post):
    post = make_post(user, title="Readable")
    login(client)
    resp = client.get(f"/post/{post.id}")
    assert resp.status_code == 200
    assert b"Readable" in resp.data


def test_view_missing_post_404(client, user):
    login(client)
    resp = client.get("/post/9999")
    assert resp.status_code == 404


def test_add_comment(client, user, make_post):
    post = make_post(user)
    login(client)
    resp = client.post(
        f"/post/{post.id}",
        data={"content": "Great post!"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert Comment.query.filter_by(body="Great post!").first() is not None


def test_update_post_by_author(client, user, make_post):
    post = make_post(user, title="Old Title")
    login(client)
    resp = client.post(
        f"/post/{post.id}/update",
        data={"title": "New Title", "content": "New body"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert Post.query.get(post.id).title == "New Title"


def test_update_post_get_prefills(client, user, make_post):
    post = make_post(user, title="Prefill Me")
    login(client)
    resp = client.get(f"/post/{post.id}/update")
    assert resp.status_code == 200
    assert b"Prefill Me" in resp.data


def test_update_post_forbidden_for_non_author(client, make_user, make_post):
    author = make_user(username="author", email="author@example.com")
    make_user(username="intruder", email="intruder@example.com")
    post = make_post(author)
    login(client, email="intruder@example.com")
    resp = client.post(
        f"/post/{post.id}/update",
        data={"title": "Hijack", "content": "nope"},
    )
    assert resp.status_code == 403


def test_delete_post_by_author(client, user, make_post):
    post = make_post(user)
    post_id = post.id
    login(client)
    resp = client.post(f"/post/{post_id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert Post.query.get(post_id) is None


def test_delete_post_forbidden_for_non_author(client, make_user, make_post):
    author = make_user(username="author2", email="author2@example.com")
    make_user(username="intruder2", email="intruder2@example.com")
    post = make_post(author)
    login(client, email="intruder2@example.com")
    resp = client.post(f"/post/{post.id}/delete")
    assert resp.status_code == 403


def test_delete_post_requires_login(client, user, make_post):
    post = make_post(user)
    resp = client.post(f"/post/{post.id}/delete")
    assert resp.status_code == 302
