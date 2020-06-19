import os
import pytest
import mock


@pytest.mark.asyncio
async def test_load_cwd(mock_hub, hub):
    with mock.patch("os.getcwd", return_value="/path"):
        mock_hub.grains.system.path.load_cwd = hub.grains.system.path.load_cwd
        await mock_hub.grains.system.path.load_cwd()
    assert mock_hub.grains.GRAINS.cwd == "/path"


@pytest.mark.asyncio
async def test_load_executable(mock_hub, hub):
    mock_hub.grains.system.path.load_executable = hub.grains.system.path.load_executable
    await mock_hub.grains.system.path.load_executable()
    assert "python" in mock_hub.grains.GRAINS.pythonexecutable


@pytest.mark.asyncio
async def test_load_path(mock_hub, hub):
    with mock.patch.dict(os.environ, {"PATH": "/path:/other/path"}):
        mock_hub.grains.system.path.load_path = hub.grains.system.path.load_path
        await mock_hub.grains.system.path.load_path()
    assert mock_hub.grains.GRAINS.path == "/path:/other/path"


@pytest.mark.asyncio
async def test_load_pythonpath(mock_hub, hub):
    mock_hub.grains.system.path.load_pythonpath = hub.grains.system.path.load_pythonpath
    await mock_hub.grains.system.path.load_pythonpath()


@pytest.mark.asyncio
async def test_load_shell(mock_hub, hub):
    with mock.patch.dict(os.environ, {"SHELL": "/bin/test_sh"}):
        mock_hub.grains.system.path.load_shell = hub.grains.system.path.load_shell
        await mock_hub.grains.system.path.load_shell()
    assert mock_hub.grains.GRAINS.shell == "/bin/test_sh"
