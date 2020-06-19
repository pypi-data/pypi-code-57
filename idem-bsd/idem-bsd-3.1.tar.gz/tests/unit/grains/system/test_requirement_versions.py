import pytest
import sys


@pytest.mark.asyncio
async def test_load_pip_versions(mock_hub, hub):

    mock_hub.grains.system.requirement_versions.load_pip_versions = (
        hub.grains.system.requirement_versions.load_pip_versions
    )

    await mock_hub.grains.system.requirement_versions.load_pip_versions()

    missing_reqs = {
        "aiofiles",
        "grainsv2",
        "dnspython",
        "idem",
        "ifcfg",
        "pop",
        "pop-config",
        "rend",
    } - mock_hub.grains.GRAINS.requirement_versions._dict().keys()
    assert not missing_reqs


@pytest.mark.asyncio
async def test_load_python_version(mock_hub, hub):

    origin = sys.version_info
    sys.version_info = (1, 2, 3)
    mock_hub.grains.system.requirement_versions.load_python_version = (
        hub.grains.system.requirement_versions.load_python_version
    )
    await mock_hub.grains.system.requirement_versions.load_python_version()
    sys.version_info = origin

    assert mock_hub.grains.GRAINS.pythonversion == (1, 2, 3)
