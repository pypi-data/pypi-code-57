import idem_linux.grains.uname
import os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_uname(mock_hub):
    with mock.patch.object(
        os,
        "uname",
        return_value=("Linux", "testname", "testrelease", "testversion", "testarch",),
    ):
        await idem_linux.grains.uname.load_uname(mock_hub)

    assert mock_hub.grains.GRAINS.kernel == "Linux"
    assert mock_hub.grains.GRAINS.nodename == "testname"
    assert mock_hub.grains.GRAINS.kernelrelease == "testrelease"
    assert mock_hub.grains.GRAINS.kernelversion == "testversion"
    assert mock_hub.grains.GRAINS.cpuarch == "testarch"
