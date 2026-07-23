from flaskblog import db
from flaskblog.models import User, Comment, load_user


def test_user_repr(user):
    assert repr(user) == "User('tester' , 'tester@example.com' , 'default.jpg')"


def test_user_default_image_file(user):
    assert user.image_file == "default.jpg"


def test_post_repr(user, make_post):
    post = make_post(user, title="Hello")
    assert repr(post).startswith("Post('Hello' , ")


def test_comment_repr(app, user, make_post):
    post = make_post(user)
    comment = Comment(body="Nice!", user_id=user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    assert repr(comment).startswith("Comment('Nice!,")


def test_load_user_returns_user(app, user):
    assert load_user(str(user.id)).id == user.id


def test_load_user_unknown_returns_none(app):
    assert load_user("9999") is None


def test_reset_token_roundtrip(app, user):
    token = user.get_reset_token()
    assert isinstance(token, str)
    assert User.verify_reset_token(token).id == user.id


def test_verify_reset_token_invalid_returns_none(app):
    assert User.verify_reset_token("not-a-real-token") is None


def test_post_author_relationship(user, make_post):
    post = make_post(user)
    assert post.author == user
    assert post in user.posts


def test_comment_cascade_delete(app, user, make_post):
    post = make_post(user)
    comment = Comment(body="to be deleted", user_id=user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    comment_id = comment.id

    db.session.delete(post)
    db.session.commit()

    assert Comment.query.get(comment_id) is None
