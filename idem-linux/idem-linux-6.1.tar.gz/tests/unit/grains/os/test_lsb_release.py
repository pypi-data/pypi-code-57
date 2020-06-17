import idem_linux.grains.os.lsb_release
import pytest


@pytest.mark.asyncio
async def test_load_lsb_release(mock_hub):
    # TODO LSB_RELEASE needs a refactor, test it more thoroughly when it's refactored
    await idem_linux.grains.os.lsb_release.load_lsb_release(mock_hub)
