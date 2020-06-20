import mock
import pytest


def test_cli(hub):
    with mock.patch("sys.argv", ["grains"]):
        hub.grains.init.cli()


def test_standalone(hub):
    hub.grains.init.standalone()


@pytest.mark.asyncio
async def test_collect(hub):
    await hub.grains.init.collect()


def test_release(hub):
    hub.grains.init.release()


def test_release_all(hub):
    hub.grains.init.release_all()


@pytest.mark.asyncio
def test_run_sub(hub):
    hub.grains.init.run_sub(hub.grains)


@pytest.mark.asyncio
async def test_process_subs(hub):
    await hub.grains.init.process_subs()


@pytest.mark.asyncio
async def test_wait_for(hub):
    hub.grains.GRAINS["new_test_grain"] = True
    await hub.grains.init.wait_for("new_test_grain")


@pytest.mark.asyncio
async def test_clean_value(hub):
    value = "123456789"
    ret = await hub.grains.init.clean_value("safe_keyword", value)
    assert value == ret
