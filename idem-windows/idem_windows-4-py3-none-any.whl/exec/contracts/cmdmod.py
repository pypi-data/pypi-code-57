# -*- coding: utf-8 -*-
import asyncio
import os
import re
import shlex
import traceback
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
        cwd = os.path.expanduser("~")

        # make sure we can access the cwd
        # when run from sudo or another environment where the euid is
        # changed ~ will expand to the home of the original uid and
        # the euid might not have access to it. See issue #1844
        if not os.access(cwd, os.R_OK):
            cwd = os.path.abspath(os.sep)
    else:
        # Handle edge cases where numeric/other input is entered, and would be
        # yaml-ified into non-string types
        cwd = str(cwd)

    if not os.path.isabs(cwd) or not os.path.isdir(cwd):
        raise SystemError(
            f"Specified cwd '{cwd}' either not absolute or does not exist"
        )

    return cwd


async def _escape_for_cmd_exe(hub, arg: str) -> str:
    """
    Escape an argument string to be suitable to be passed to
    cmd.exe on Windows

    This method takes an argument that is expected to already be properly
    escaped for the receiving program to be properly parsed. This argument
    will be further escaped to pass the interpolation performed by cmd.exe
    unchanged.

    Any meta-characters will be escaped, removing the ability to e.g. use
    redirects or variables.

    Args:
        arg (str): a single command line argument to escape for cmd.exe

    Returns:
        str: an escaped string suitable to be passed as a program argument to cmd.exe
    """
    meta_chars = '()%!^"<>&|'
    meta_re = re.compile(
        "(" + "|".join(re.escape(char) for char in list(meta_chars)) + ")"
    )
    meta_map = {char: "^{0}".format(char) for char in meta_chars}

    def escape_meta_chars(m):
        char = m.group(1)
        return meta_map[char]

    return meta_re.sub(escape_meta_chars, arg)


async def _escape_argument(hub, arg: str, escape: bool = True):
    """
    Escape the argument for the cmd.exe shell.
    See http://blogs.msdn.com/b/twistylittlepassagesallalike/archive/2011/04/23/everyone-quotes-arguments-the-wrong-way.aspx

    First we escape the quote chars to produce a argument suitable for
    CommandLineToArgvW. We don't need to do this for simple arguments.

    Args:
        arg (str): a single command line argument to escape for the cmd.exe shell

    Kwargs:
        escape (bool): True will call the escape_for_cmd_exe() function
                       which escapes the characters '()%!^"<>&|'. False
                       will not call the function and only quotes the cmd

    Returns:
        str: an escaped string suitable to be passed as a program argument to the cmd.exe shell
    """
    if not arg or re.search(r'(["\s])', arg):
        arg = '"' + arg.replace('"', r"\"") + '"'

    if not escape:
        return arg
    return await _escape_for_cmd_exe(hub, arg)


async def _sanitize_cmd(hub, cmd: str or List[str]) -> str or List[str]:
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    # Return stripped command string copies to improve logging.
    # Use shlex.quote to properly escape whitespace and special characters in strings passed to shells
    return [await _escape_for_cmd_exe(hub, x) for x in cmd]


async def _sanitize_kwargs(hub, **kwargs):
    """
    Only pass through approved kwargs
    """
    new_kwargs = {}
    if "stdin_raw_newlines" in kwargs:
        new_kwargs["stdin_raw_newlines"] = kwargs["stdin_raw_newlines"]
    return new_kwargs


async def call_run(hub, ctx):
    kwargs = ctx.get_arguments()
    shell = kwargs.get("shell")
    cmd = kwargs["cmd"]

    if shell:
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
    else:
        cmd = await _sanitize_cmd(hub, cmd)
    new_kwargs = {
        "cmd": cmd,
        "cwd": await _sanitize_cwd(hub, kwargs["cwd"]),
        "env": await _sanitize_env(hub, ctx.kwargs.get("env", os.environ.copy())),
        "stdout": kwargs.get("stdout"),
        "stderr": kwargs.get("stderr"),
        "shell": shell,
        "timeout": kwargs.get("timeout"),
    }
    new_kwargs.update(await _sanitize_kwargs(hub, **new_kwargs))

    return await ctx.func(hub, **new_kwargs)


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


async def _powershell_mod(hub, cmd: str or List[str]) -> str or List[str]:
    # If we were called by script(), then fakeout the Windows
    # shell to run a Powershell script.
    # Else just run a Powershell command.
    stack = traceback.extract_stack(limit=2)

    # extract_stack() returns a list of tuples.
    # The last item in the list [-1] is the current method.
    # The third item[2] in each tuple is the name of that method.
    if stack[-2][2] == "script":
        return (
            f"Powershell -NonInteractive -NoProfile -ExecutionPolicy Bypass -File {cmd}"
        )
    else:
        return 'Powershell -NonInteractive -NoProfile "{0}"'.format(
            cmd.replace('"', '\\"')
        )


async def call_powershell(hub, ctx):
    kwargs = ctx.get_arguments
    cmd = await _powershell_mod(hub, kwargs.pop("cmd"))
    yield await ctx.func(hub, cmd=cmd, **kwargs)
