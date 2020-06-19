import pytest
import mock


@pytest.mark.asyncio
async def test_load_pid(mock_hub, hub):
    ret = 1234
    with mock.patch("os.getpid", return_value=ret):
        mock_hub.grains.proc.pid.load_pid = hub.grains.proc.pid.load_pid
        await mock_hub.grains.proc.pid.load_pid()

    assert mock_hub.grains.GRAINS.pid == ret
