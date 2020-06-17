import idem_linux.grains.system.machine_id
import io
import pytest
import mock


@pytest.mark.asyncio
async def test_load_machine_id(mock_hub):
    with mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("999999999999999999ffffffffffffff"),
    ):
        await idem_linux.grains.system.machine_id.load_machine_id(mock_hub)
    await idem_linux.grains.system.machine_id.load_machine_id(mock_hub)
