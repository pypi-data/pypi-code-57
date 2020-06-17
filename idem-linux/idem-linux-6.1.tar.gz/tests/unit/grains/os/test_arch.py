import idem_linux.grains.os.arch
import os
import pytest
import shutil
import mock
from dict_tools import data


@pytest.mark.asyncio
async def test_get_osarch_uname(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test_arch"})

    with mock.patch.object(shutil, "which", side_effect=[True]):
        await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"


@pytest.mark.asyncio
async def test_get_osarch_rpm(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test_arch"})

    with mock.patch.dict(os.environ, {"_host_cpu": "True"}):
        with mock.patch.object(shutil, "which", side_effect=[False, True]):
            await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"


@pytest.mark.asyncio
async def test_get_osarch_opkg(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "foo\narch test_arch 64"}
    )

    with mock.patch.object(shutil, "which", side_effect=[False, False, True]):
        await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"


@pytest.mark.asyncio
async def test_get_osarch_dpkg(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test_arch"})

    with mock.patch.object(shutil, "which", side_effect=[False, False, False, True]):
        await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"


@pytest.mark.asyncio
async def test_get_osarch_6432(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test_arch"})

    with mock.patch.object(shutil, "which", side_effect=[False, False, False, False]):
        with mock.patch.dict(os.environ, {"PROCESSOR_ARCHITEW6432": "test_arch"}):
            await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"


@pytest.mark.asyncio
async def test_get_osarch(mock_hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "test_arch"})

    with mock.patch.object(shutil, "which", side_effect=[False, False, False, False]):
        with mock.patch.dict(os.environ, {"PROCESSOR_ARCHITECTURE": "test_arch"}):
            await idem_linux.grains.os.arch.get_osarch(mock_hub)

    assert mock_hub.grains.GRAINS.osarch == "test_arch"
