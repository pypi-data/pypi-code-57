# -*- coding: utf-8 -*-
import asyncio
import functools
import os
import shlex
from typing import Any, Dict, List

__virtualname__ = "cmd"


async def _sanitize_env(hub, env: Dict[str, Any]) -> Dict[str, str] or None:
    if env is None:
        return
    for bad_env_key in (k for k, v in env.items() if v is None):
        hub.log.error(
            "Environment variable '%s' passed without a value. "
            "Setting value to an empty string",
            bad_env_key,
        )
        env[bad_env_key] = ""
    return env


async def _sanitize_cwd(hub, cwd: str or None) -> str:
    # salt-minion is running as. Defaults to home directory of user under which
    # the minion is running.
    if not cwd:
        cwd = os.getcwd()

        # make sure we can access the cwd
        # when run from sudo or another environment where the euid is
        # changed ~ will expand to the home of the original uid and
        # the euid might not have access to it. See issue #1844
        if not os.access(cwd, os.R_OK):
            cwd = "/"
    else:
        # Handle edge cases where numeric/other input is entered, and would be
        # yaml-ified into non-string types
        cwd = str(cwd)

    if not os.path.isabs(cwd) or not os.path.isdir(cwd):
        raise SystemError(
            f"Specified cwd '{cwd}' either not absolute or does not exist"
        )

    return cwd


async def _sanitize_cmd(hub, cmd: str or List[str]) -> str or List[str]:
    if not isinstance(cmd, list):
        cmd = cmd.split()

    # Use shlex.quote to properly escape whitespace and special characters in strings passed to shells
    if isinstance(cmd, list):
        cmd = [shlex.quote(str(x).strip()) for x in cmd]
    else:
        cmd = shlex.quote(cmd)
    return cmd


async def _sanitize_umask(hub, umask: str) -> int or None:
    if umask is None:
        return

    _umask = str(umask).lstrip("0")

    if _umask == "":
        raise SystemError("Zero umask is not allowed.")

    try:
        return int(_umask, 8)
    except ValueError:
        raise SystemError("Invalid umask: '{0}'".format(umask))


async def _sanitize_kwargs(hub, **kwargs):
    """
    Only pass through approved kwargs
    """
    new_kwargs = {}
    if "stdin_raw_newlines" in kwargs:
        new_kwargs["stdin_raw_newlines"] = kwargs["stdin_raw_newlines"]
    return new_kwargs


async def call_run(hub, ctx):
    umask = ctx.kwargs.get("umask")
    shell = ctx.kwargs.get("shell")
    cmd = ctx.kwargs.get("cmd", ctx.args.pop(1))
    if shell:
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
    else:
        cmd = await _sanitize_cmd(hub, cmd)
    kwargs = {
        "cmd": cmd,
        "cwd": await _sanitize_cwd(
            hub, ctx.kwargs.get("cwd", ctx.args.pop(1) if len(ctx.args) > 1 else None)
        ),
        "env": await _sanitize_env(hub, ctx.kwargs.get("env", os.environ.copy())),
        "preexec_fn": functools.partial(os.umask, await _sanitize_umask(hub, umask))
        if umask
        else None,
        "stdout": ctx.kwargs.get("stdout", asyncio.subprocess.PIPE),
        "stderr": ctx.kwargs.get("stderr", asyncio.subprocess.PIPE),
        "shell": shell,
        "timeout": ctx.kwargs.get("timeout"),
    }
    kwargs.update(await _sanitize_kwargs(hub, **kwargs))

    return await ctx.func(*ctx.args, **kwargs)


async def sig_run(
    hub,
    cmd: str or List[str],
    cwd: str = None,
    shell: bool = False,
    stdin: str = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    env: Dict[str, Any] = None,
    timeout: int or float = None,
    **kwargs,
) -> Dict[str, Any]:
    pass
