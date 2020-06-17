import glob
import idem_linux.grains.net.fibre_channel
import io
import pytest
import mock


@pytest.mark.asyncio
async def test_load_wwn(mock_hub):
    with mock.patch.object(
        glob,
        "glob",
        return_value=[f"/sys/class/fc_host/host{num}/port_name" for num in range(6)],
    ):
        with mock.patch(
            "aiofiles.threadpool.sync_open",
            side_effect=[
                io.StringIO("0x21000024ff123311"),
                io.StringIO("0x21000024ff123312"),
                io.StringIO("0x21000024ff123313"),
                io.StringIO("0x21000024ff123314"),
                io.StringIO("0x21000024ff123315"),
                io.StringIO("0x21000024ff123316"),
            ],
        ):
            await idem_linux.grains.net.fibre_channel.load_wwn(mock_hub)

    assert mock_hub.grains.GRAINS.fc_wwn == (
        "21000024ff123311",
        "21000024ff123312",
        "21000024ff123313",
        "21000024ff123314",
        "21000024ff123315",
        "21000024ff123316",
    )
