import glob
import idem_linux.grains.hw.storage.disks
import io
import os.path
import pytest
import mock

DISK_DATA = """
"""


@pytest.mark.asyncio
async def test_load_disks(mock_hub):
    with mock.patch.object(os.path, "exists", return_value=True):
        with mock.patch.object(
            glob,
            "glob",
            return_value=[
                f"/sys/blcok/test-disk{num}/queue/rotational" for num in range(6)
            ],
        ):
            with mock.patch(
                "aiofiles.threadpool.sync_open",
                side_effect=[
                    io.StringIO("0"),  # SSD
                    io.StringIO("0"),  # SSD
                    io.StringIO("0"),  # SSD
                    io.StringIO("1"),  # HDD
                    io.StringIO("1"),  # HDD
                    io.StringIO("1"),  # HDD
                ],
            ):
                await idem_linux.grains.hw.storage.disks.load_disks(mock_hub)

    assert mock_hub.grains.GRAINS.SSDs == ("test-disk0", "test-disk1", "test-disk2")
    assert mock_hub.grains.GRAINS.disks == ("test-disk3", "test-disk4", "test-disk5")
