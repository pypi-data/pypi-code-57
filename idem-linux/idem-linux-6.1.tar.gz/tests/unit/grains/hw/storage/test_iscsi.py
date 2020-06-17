import idem_linux.grains.hw.storage.iscsi
import io
import os.path
import pytest
import mock


ISCSI_DATA = """
InitiatorName=iqn.2005-03.org.open-iscsi:3f5058b1d0a0
InitiatorName=iqn.2006-04.com.example.node1
"""


@pytest.mark.asyncio
async def test_load_iqn(mock_hub):
    with mock.patch.object(os.path, "exists", return_value=True):
        with mock.patch(
            "aiofiles.threadpool.sync_open", return_value=io.StringIO(ISCSI_DATA)
        ):
            await idem_linux.grains.hw.storage.iscsi.load_iqn(mock_hub)

    assert mock_hub.grains.GRAINS.iscsi_iqn == (
        "iqn.2005-03.org.open-iscsi:3f5058b1d0a0",
        "iqn.2006-04.com.example.node1",
    )
