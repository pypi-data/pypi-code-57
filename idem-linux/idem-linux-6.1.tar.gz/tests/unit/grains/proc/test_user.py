import idem_linux.grains.proc.user
import pytest
import os
import pwd
import mock


@pytest.mark.asyncio
async def test_load_user(mock_hub):
    ret = 1234
    lam = lambda: 0
    lam.pw_name = "test_user"
    with mock.patch.object(os, "geteuid", return_value=ret):
        with mock.patch.object(pwd, "getpwuid", return_value=lam):
            await idem_linux.grains.proc.user.load_user(mock_hub)

    assert mock_hub.grains.GRAINS.uid == ret
    assert mock_hub.grains.GRAINS.username == "test_user"
