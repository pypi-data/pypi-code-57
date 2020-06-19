import collections.abc
import asyncio
import pytest


class TestCmd:
    @pytest.mark.asyncio
    async def test_run(self, hub):
        ret = await hub.exec.cmd.run("pwd")
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout.strip().split(), "No output from command"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_error(self, hub):
        try:
            await hub.exec.cmd.run("nonexistent_command")
        except FileNotFoundError:
            return
        assert False, "Command execution should have failed"

    @pytest.mark.asyncio
    async def test_run_string_list(self, hub):
        ret = await hub.exec.cmd.run("ls -la")
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout, "No output from command"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_list(self, hub):
        ret = await hub.exec.cmd.run(["ls", "-la"])
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout, "No output from command"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_shell(self, hub):
        ret = await hub.exec.cmd.run("pwd", shell=True)
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout, "No output from command"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_cwd(self, hub):
        ret = await hub.exec.cmd.run(["pwd"], cwd="/")
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout.strip() == "/"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_cwd_fail(self, hub):
        try:
            await hub.exec.cmd.run(["pwd"], cwd="/nonexistant_path")
        except SystemError:
            return
        assert False, "Expected a system error with a pad path"

    @pytest.mark.asyncio
    async def test_run_env(self, hub):
        env = {"test_env_attr": "test_env_val", "another": "value"}
        ret = await hub.exec.cmd.run("env", env=env)
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout.strip() == "\n".join(f"{k}={v}" for k, v in env.items())
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_timeout(self, hub):
        ret = await hub.exec.cmd.run("pwd", timeout=1)
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout.strip(), "No output from command"
        assert not ret.stderr

    @pytest.mark.asyncio
    async def test_run_timeout_fail(self, hub):
        try:
            await hub.exec.cmd.run(["sleep", "5"], timeout=0)
        except asyncio.TimeoutError:
            return

        assert False, "Timeout should have been reached"

    @pytest.mark.asyncio
    async def test_run_umask(self, hub):
        ret = await hub.exec.cmd.run("pwd", umask="666")
        assert isinstance(ret, collections.abc.Mapping)
        assert ret.keys() == {"pid", "retcode", "stdout", "stderr"}
        assert ret.retcode == 0
        assert ret.stdout.strip(), "No output from command"
        assert not ret.stderr
