import idem_linux.grains.proc.pid
import pytest
import os
import mock


@pytest.mark.asyncio
async def test_load_pid(mock_hub):
    ret = 1234
    with mock.patch.object(os, "getpid", return_value=ret):
        await idem_linux.grains.proc.pid.load_pid(mock_hub)

    assert mock_hub.grains.GRAINS.pid == ret
