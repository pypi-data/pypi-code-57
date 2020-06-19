import io
import pytest
import mock


@pytest.mark.asyncio
async def test_load_machine_id(mock_hub, hub):
    mock_hub.grains.system.machine_id.load_machine_id = (
        hub.grains.system.machine_id.load_machine_id
    )
    with mock.patch(
        "aiofiles.threadpool.sync_open",
        return_value=io.StringIO("999999999999999999ffffffffffffff"),
    ):
        await mock_hub.grains.system.machine_id.load_machine_id()

    assert mock_hub.grains.GRAINS.machine_id == "999999999999999999ffffffffffffff"
