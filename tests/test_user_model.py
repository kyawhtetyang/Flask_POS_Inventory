from models.user import User


def test_add_and_authenticate_user(tmp_path):
    db_path = tmp_path / "test_shop.db"
    users = User(str(db_path))

    users.add_user("alice", "s3cret", "Manager")
    user = users.authenticate("alice", "s3cret")

    assert user is not None
    assert user["username"] == "alice"
    assert user["role"] == "Manager"
