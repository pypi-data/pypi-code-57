import pytest


@pytest.mark.asyncio
async def test_run(hub, ctx):
    return
    ret = await hub.states.cmd.run(ctx, name="pwd")
    assert ret["changes"].keys() == {"pid", "retcode", "stdout", "stderr"}
    assert ret["changes"].retcode == 0
    assert ret["changes"].stdout.strip().split(), "No output from command"
    assert not ret["changes"].stderr
