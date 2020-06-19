import pytest
import mock


@pytest.mark.asyncio
async def test_load_uname(mock_hub, hub):
    with mock.patch(
        "os.uname",
        return_value=("TestBSD", "testname", "testrelease", "testversion", "testarch",),
    ):
        mock_hub.grains.uname.load_uname = hub.grains.uname.load_uname
        await mock_hub.grains.uname.load_uname()

    assert mock_hub.grains.GRAINS.kernel == "TestBSD"
    assert mock_hub.grains.GRAINS.nodename == "testname"
    assert mock_hub.grains.GRAINS.kernelrelease == "testrelease"
    assert mock_hub.grains.GRAINS.kernelversion == "testversion"
    assert mock_hub.grains.GRAINS.osarch == "testarch"

    # Hard coded grains
    assert mock_hub.grains.GRAINS.os_family == "BSD"
    assert mock_hub.grains.GRAINS.ps == "ps auxwww"
