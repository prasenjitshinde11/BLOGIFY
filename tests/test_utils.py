from unittest.mock import MagicMock, patch

from flaskblog.users import utils


def buffer_storage(filename):
    storage = MagicMock()
    storage.filename = filename
    return storage


def test_save_picture_returns_hashed_filename(app):
    fake_user = MagicMock()
    fake_user.image_file = "default.jpg"

    with patch.object(utils, "Image") as mock_image, patch(
        "flask_login.current_user", fake_user
    ):
        mock_image.open.return_value = MagicMock()
        result = utils.save_picture(buffer_storage("photo.png"))

    # 8 random bytes -> 16 hex chars, plus the original extension.
    assert result.endswith(".png")
    assert len(result) == 16 + len(".png")


def test_save_picture_deletes_old_non_default(app):
    fake_user = MagicMock()
    fake_user.image_file = "old_pic.png"

    with patch.object(utils, "Image") as mock_image, patch(
        "flask_login.current_user", fake_user
    ), patch.object(utils.os.path, "exists", return_value=True), patch.object(
        utils.os, "remove"
    ) as mock_remove:
        thumb = MagicMock()
        mock_image.open.return_value = thumb

        result = utils.save_picture(buffer_storage("new.png"))

    assert mock_remove.called
    assert result.endswith(".png")


def test_save_picture_keeps_default(app):
    fake_user = MagicMock()
    fake_user.image_file = "default.jpg"

    with patch.object(utils, "Image") as mock_image, patch(
        "flask_login.current_user", fake_user
    ), patch.object(utils.os, "remove") as mock_remove:
        mock_image.open.return_value = MagicMock()
        utils.save_picture(buffer_storage("new.png"))

    assert not mock_remove.called


def test_send_reset_email_sends_message(app, user):
    with patch.object(utils, "mail") as mock_mail:
        utils.send_reset_email(user)

    assert mock_mail.send.called
    sent_msg = mock_mail.send.call_args[0][0]
    assert user.email in sent_msg.recipients
    assert "reset your password" in sent_msg.body.lower()
