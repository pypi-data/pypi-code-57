import idem_linux.grains.system.requirement_versions
import pytest
import sys


@pytest.mark.asyncio
async def test_load_pip_versions(mock_hub):

    await idem_linux.grains.system.requirement_versions.load_pip_versions(mock_hub)

    missing_reqs = {
        "aiofiles",
        "grainsv2",
        "distro",
        "dnspython",
        "idem",
        "pop",
        "pop-config",
        "rend",
    } - mock_hub.grains.GRAINS.requirement_versions._dict().keys()
    assert not missing_reqs


@pytest.mark.asyncio
async def test_load_python_version(mock_hub):

    origin = sys.version_info
    sys.version_info = (1, 2, 3)
    await idem_linux.grains.system.requirement_versions.load_python_version(mock_hub)
    sys.version_info = origin

    assert mock_hub.grains.GRAINS.pythonversion == (1, 2, 3)
