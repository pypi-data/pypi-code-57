import idem_linux.grains.system.console
import getpass
import pytest
import pwd
import mock


@pytest.mark.asyncio
async def test_load_console_user(mock_hub):
    ret = lambda: 0
    ret.pw_uid = 999
    with mock.patch.object(getpass, "getuser", return_value="test_user"):
        with mock.patch.object(pwd, "getpwnam", return_value=ret):
            await idem_linux.grains.system.console.load_console_user(mock_hub)

    assert mock_hub.grains.GRAINS.console_username == "test_user"
    assert mock_hub.grains.GRAINS.console_user == 999
