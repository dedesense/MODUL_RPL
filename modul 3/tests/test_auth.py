import hashlib
from unittest.mock import MagicMock

from models.user_model import UserModel


def test_hash_password_is_consistent_sha256():
    model = UserModel()
    password = "admin123"
    expected_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    assert model.hash_password(password) == expected_hash
    assert model.hash_password(password) == model.hash_password(password)
    assert len(model.hash_password(password)) == 64


def test_login_returns_user_when_credentials_match():
    model = UserModel()
    connection = MagicMock()
    cursor = MagicMock()
    user = {"id": 1, "username": "petugas", "role": "admin"}
    cursor.fetchone.return_value = user
    connection.cursor.return_value = cursor
    model.db = MagicMock()
    model.db.connect.return_value = connection

    result = model.login("petugas", "admin123")

    expected_hash = hashlib.sha256(b"admin123").hexdigest()
    cursor.execute.assert_called_once_with(
        "SELECT id_user AS id, username, role FROM users WHERE username = %s AND password = %s",
        ("petugas", expected_hash),
    )
    assert result == user
    cursor.close.assert_called_once()
    connection.close.assert_called_once()
