import grains.grains.init as grains
import pytest


def test_init(hub):
    mock_hub = hub.pop.testing.mock_hub()
    grains.__init__(mock_hub)
    mock_hub.pop.sub.load_subdirs.assert_called_once_with(mock_hub.grains, recurse=True)
    mock_hub.pop.data.omap.assert_called_once_with()


def test_cli(hub):
    """
    Test getting option from the target
    """
    mock_hub = hub.pop.testing.mock_hub()
    mock_hub.OPT = hub.pop.data.omap(
        {"grains": {"grains": []}, "rend": {"output": "nested"}}
    )
    grains.cli(mock_hub)

    mock_hub.pop.config.load.assert_called_once()
    mock_hub.grains.init.standalone.assert_called_once_with()


def test_standalone(hub):
    mock_hub = hub.pop.testing.mock_hub()
    grains.standalone(mock_hub)
    mock_hub.pop.loop.start.assert_called_once()
    mock_hub.grains.init.collect.assert_called_once_with()


@pytest.mark.asyncio
async def test_collect(mock_hub):
    await grains.collect(mock_hub)

    mock_hub.grains.init.process_subs.assert_called_once()


def test_release(mock_hub):
    mock_hub.grains.init.release()


def test_release_all(mock_hub):
    mock_hub.grains.init.release_all()


def test_run_sub(mock_hub):
    grains.run_sub(mock_hub, [])


@pytest.mark.asyncio
async def test_process_subs(hub):
    mock_hub = hub.pop.testing.mock_hub()
    await grains.process_subs(mock_hub)
    mock_hub.pop.sub.iter_subs.assert_called_once_with(mock_hub.grains, recurse=True)


@pytest.mark.asyncio
async def test_wait_for(mock_hub):
    mock_hub.grains.GRAINS["new_test_grain"] = True
    await mock_hub.grains.init.wait_for("new_test_grain")


@pytest.mark.asyncio
async def test_clean_value(mock_hub):
    await mock_hub.grains.init.clean_value("", "")
