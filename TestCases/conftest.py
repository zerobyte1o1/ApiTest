from support.user import User
import pytest


@pytest.fixture(scope="session")
def admin():
    return User("admin", "teletraan")
