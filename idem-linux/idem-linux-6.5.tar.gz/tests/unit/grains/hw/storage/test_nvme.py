import idem_linux.grains.hw.storage.nvme
import io
import os.path
import pytest
import mock

NQN_DATA = """
nqn.testnqn:234236
nqn.testnqn.test:23958
"""


@pytest.mark.asyncio
async def test_load_nvme_nqn(mock_hub):
    with mock.patch.object(os.path, "exists", return_value=True):
        with mock.patch(
            "aiofiles.threadpool.sync_open", return_value=io.StringIO(NQN_DATA)
        ):
            await idem_linux.grains.hw.storage.nvme.load_nvme_nqn(mock_hub)

    assert mock_hub.grains.GRAINS.nvme_nqn == (
        "nqn.testnqn:234236",
        "nqn.testnqn.test:23958",
    )
