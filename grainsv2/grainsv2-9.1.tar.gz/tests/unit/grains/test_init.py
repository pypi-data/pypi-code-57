import pytest


def test_init(mock_hub, hub):
    mock_hub.pop.sub.add = hub.pop.sub.add
    mock_hub.grains.init.__init__ = hub.grains.init.__init__
    mock_hub._subs = hub._subs
    mock_hub._dscan = hub._dscan
    mock_hub._dynamic = hub._dynamic

    mock_hub.pop.sub.add(dyne_name="grains")

    mock_hub.pop.sub.load_subdirs.assert_called_with(mock_hub.grains, recurse=True)


def test_cli(mock_hub, hub):
    """
    Test getting option from the target
    """
    mock_hub.grains.init.cli = hub.grains.init.cli
    mock_hub.OPT = hub.pop.data.omap(
        {"grains": {"grains": []}, "rend": {"output": "nested"}}
    )
    mock_hub.grains.init.cli()

    mock_hub.pop.config.load.assert_called_once()
    mock_hub.grains.init.standalone.assert_called_once_with()


def test_standalone(mock_hub, hub):
    mock_hub.grains.init.standalone = hub.grains.init.standalone

    mock_hub.grains.init.standalone()

    mock_hub.pop.loop.start.assert_called_once()
    mock_hub.grains.init.collect.assert_called_once_with()


@pytest.mark.asyncio
async def test_collect(mock_hub, hub):
    mock_hub.grains.init.collect = hub.grains.init.collect
    await mock_hub.grains.init.collect()

    mock_hub.grains.init.process_subs.assert_called_once()


def test_release(mock_hub, hub):
    mock_hub.grains.init.release = hub.grains.init.release
    mock_hub.grains.init.release()


def test_release_all(mock_hub, hub):
    mock_hub.grains.init.release_all = hub.grains.init.release_all
    mock_hub.grains.init.release_all()


def test_run_sub(mock_hub, hub):
    mock_hub.grains.init.run_sub = hub.grains.init.run_sub
    mock_hub.grains.init.run_sub([])


@pytest.mark.asyncio
async def test_process_subs(mock_hub, hub):
    mock_hub.grains.init.process_subs = hub.grains.init.process_subs

    await mock_hub.grains.init.process_subs()

    mock_hub.pop.sub.iter_subs.assert_called_once_with(mock_hub.grains, recurse=True)


@pytest.mark.asyncio
async def test_wait_for(mock_hub, hub):
    mock_hub.grains.init.wait_for = hub.grains.init.wait_for

    hub.grains.GRAINS["new_test_grain"] = True
    mock_hub.grains.init.wait_for("new_test_grain")


@pytest.mark.asyncio
async def test_clean_value(mock_hub, hub):
    mock_hub.grains.init.clean_value = hub.grains.init.clean_value

    await mock_hub.grains.init.clean_value("", "")
