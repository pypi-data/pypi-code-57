from dict_tools import data
import pytest
import mock


@pytest.mark.asyncio
async def test_load_osbuild(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "testbuild"})

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.os.os.load_osbuild = hub.grains.os.os.load_osbuild
        await mock_hub.grains.os.os.load_osbuild()

    assert mock_hub.grains.GRAINS.osbuild == "testbuild"


@pytest.mark.asyncio
async def test_load_oscodename(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "testcodename"})

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.os.os.load_oscodename = hub.grains.os.os.load_oscodename
        await mock_hub.grains.os.os.load_oscodename()

    assert mock_hub.grains.GRAINS.oscodename == "testcodename"


@pytest.mark.asyncio
async def test_load_osinfo(mock_hub, hub):
    mock_hub.grains.GRAINS.kernel = "TestBSD"
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "1000.99-TESTING"}
    )

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.os.os.load_osinfo = hub.grains.os.os.load_osinfo
        await mock_hub.grains.os.os.load_osinfo()

    assert mock_hub.grains.GRAINS.os == "TestBSD"
    assert mock_hub.grains.GRAINS.osrelease == "1000.99"
    assert mock_hub.grains.GRAINS.osfullname == "TestBSD-1000.99-TESTING"
    assert mock_hub.grains.GRAINS.osrelease_info == (1000, 99)
    assert mock_hub.grains.GRAINS.osmajorrelease == 1000
    assert mock_hub.grains.GRAINS.osfinger == "TestBSD-1000"
