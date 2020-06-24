import os
import pytest


@pytest.fixture
def user_password_key():
    return (
        os.environ["TEST_USER"],
        os.environ["TEST_PASSWORD"],
        os.environ["TEST_API_KEY"],
    )
