from tests.conftest import login


def test_welcome_page_for_anonymous(client, user, make_post):
    make_post(user)
    resp = client.get("/")
    assert resp.status_code == 200
    # Welcome landing page is shown to anonymous visitors.
    assert b"welcome" in resp.data.lower()


def test_home_feed_for_logged_in_user(client, user, make_post):
    make_post(user, title="Visible Post")
    login(client)
    resp = client.get("/home")
    assert resp.status_code == 200
    assert b"Visible Post" in resp.data


def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200


def test_home_pagination_query_param(client, user):
    login(client)
    resp = client.get("/home?page=1")
    assert resp.status_code == 200
