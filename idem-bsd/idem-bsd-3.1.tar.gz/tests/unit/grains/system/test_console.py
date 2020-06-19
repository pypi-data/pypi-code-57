import pytest
import mock


@pytest.mark.asyncio
async def test_load_console_user(mock_hub, hub):
    ret = lambda: 0
    ret.pw_uid = 999
    with mock.patch("getpass.getuser", return_value="test_user"):
        with mock.patch("pwd.getpwnam", return_value=ret):
            mock_hub.grains.system.console.load_console_user = (
                hub.grains.system.console.load_console_user
            )
            await mock_hub.grains.system.console.load_console_user()

    assert mock_hub.grains.GRAINS.console_username == "test_user"
    assert mock_hub.grains.GRAINS.console_user == 999
