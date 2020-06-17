import idem_linux.grains.system.path
import os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_cwd(mock_hub):
    with mock.patch.object(os, "getcwd", return_value="/path"):
        await idem_linux.grains.system.path.load_cwd(mock_hub)
    assert mock_hub.grains.GRAINS.cwd == "/path"


@pytest.mark.asyncio
async def test_load_executable(mock_hub):
    await idem_linux.grains.system.path.load_executable(mock_hub)
    assert "python" in mock_hub.grains.GRAINS.pythonexecutable


@pytest.mark.asyncio
async def test_load_path(mock_hub):
    with mock.patch.dict(os.environ, {"PATH": "/path:/other/path"}):
        await idem_linux.grains.system.path.load_path(mock_hub)
    assert mock_hub.grains.GRAINS.path == "/path:/other/path"


@pytest.mark.asyncio
async def test_load_pythonpath(mock_hub):
    await idem_linux.grains.system.path.load_pythonpath(mock_hub)


@pytest.mark.asyncio
async def test_load_shell(mock_hub):
    with mock.patch.dict(os.environ, {"SHELL": "/bin/test_sh"}):
        await idem_linux.grains.system.path.load_shell(mock_hub)
    assert mock_hub.grains.GRAINS.shell == "/bin/test_sh"
