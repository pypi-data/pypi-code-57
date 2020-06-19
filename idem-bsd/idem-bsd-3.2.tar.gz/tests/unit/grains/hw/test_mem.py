from dict_tools import data
import pytest
import mock


@pytest.mark.asyncio
async def test_load_meminfo(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "9999999999"})

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.hw.mem.load_meminfo = hub.grains.hw.mem.load_meminfo
        await mock_hub.grains.hw.mem.load_meminfo()

    assert mock_hub.grains.GRAINS.mem_total == 9536


@pytest.mark.asyncio
async def test_load_meminfo64(mock_hub, hub):
    mock_hub.exec.cmd.run.side_effect = [
        data.NamespaceDict({"stdout": "-1"}),
        data.NamespaceDict({"stdout": "9999999999999999999"}),
    ]

    with mock.patch("shutil.which", return_value=True):
        mock_hub.grains.hw.mem.load_meminfo = hub.grains.hw.mem.load_meminfo
        await mock_hub.grains.hw.mem.load_meminfo()

    assert mock_hub.grains.GRAINS.mem_total == 9536743164062


@pytest.mark.asyncio
async def test_load_swap_swapctl(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict(
        {"stdout": "Total:           2617340          0"}
    )

    with mock.patch("shutil.which", side_effect=[True, False, False]):
        mock_hub.grains.hw.mem.load_swap = hub.grains.hw.mem.load_swap
        await mock_hub.grains.hw.mem.load_swap()

    assert mock_hub.grains.GRAINS.swap_total == 2555


@pytest.mark.asyncio
async def test_load_swap_sysctl(mock_hub, hub):
    mock_hub.exec.cmd.run.return_value = data.NamespaceDict({"stdout": "2680156160"})

    with mock.patch("shutil.which", side_effect=[False, True, False]):
        mock_hub.grains.hw.mem.load_swap = hub.grains.hw.mem.load_swap
        await mock_hub.grains.hw.mem.load_swap()

    assert mock_hub.grains.GRAINS.swap_total == 2555


@pytest.mark.asyncio
async def test_load_swap(mock_hub, hub):
    with mock.patch("shutil.which", side_effect=[False, False, False]):
        mock_hub.grains.hw.mem.load_swap = hub.grains.hw.mem.load_swap
        await mock_hub.grains.hw.mem.load_swap()

    assert mock_hub.grains.GRAINS.swap_total == 0
