import json
import os

import pytest

from tktl.commands.login import LogInCommand, SetApiKeyCommand
from tktl.core.exceptions import InvalidInputError


def test_set_api_key(capsys):
    cmd = SetApiKeyCommand()
    cmd.execute(api_key=None)
    out, err = capsys.readouterr()
    assert "API Key cannot be empty.\n" == err

    cmd.execute(api_key="ABC")
    assert os.path.exists(os.path.expanduser("~/.tktl/config.json"))
    with open(os.path.expanduser("~/.tktl/config.json"), "r") as j:
        d = json.load(j)
        assert d["api-key"] == "ABC"


def test_login(capsys, user_password_key):
    cmd = LogInCommand()
    with pytest.raises(InvalidInputError):
        cmd.execute(None, None, None)

    with pytest.raises(InvalidInputError):
        cmd.execute(None, "me", None)

    u, p, k = user_password_key

    assert cmd.execute(u, p, None) is True
    out, err = capsys.readouterr()
    assert out == "Login successful!\n"
    assert cmd.execute(None, None, k) is True
    out, err = capsys.readouterr()
    assert out == "Login successful!\n"

    assert cmd.execute(u, "whatever", None) is False
    out, err = capsys.readouterr()
    assert err == "Request failed: Incorrect username or password\n"
