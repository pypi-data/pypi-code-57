import pytest
import mock


@pytest.mark.asyncio
async def test_load_user(mock_hub, hub):
    ret = 1234
    lam = lambda: 0
    lam.pw_name = "test_user"
    with mock.patch("os.geteuid", return_value=ret):
        with mock.patch("pwd.getpwuid", return_value=lam):
            mock_hub.grains.proc.user.load_user = hub.grains.proc.user.load_user
            await mock_hub.grains.proc.user.load_user()

    assert mock_hub.grains.GRAINS.uid == ret
    assert mock_hub.grains.GRAINS.username == "test_user"
