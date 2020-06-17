import pytest


@pytest.mark.asyncio
async def test_run(hub, ctx):
    ret = await hub.states.cmd.run(ctx, "pwd")
    assert isinstance(ret, dict)
    assert ret["changes"].keys() == {"pid", "retcode", "stdout", "stderr"}
    assert ret["changes"].retcode == 0
    assert ret["changes"].stdout.strip().split(), "No output from command"
    assert not ret["changes"].stderr
