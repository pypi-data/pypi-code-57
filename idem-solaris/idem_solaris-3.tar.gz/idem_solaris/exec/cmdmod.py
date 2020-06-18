# -*- coding: utf-8 -*-
import asyncio
import dict_tools
from typing import Any, Dict, List

__virtualname__ = "cmd"


async def run(
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
    """
    Execute the passed command and return the output as a string

    :param cmd: The command to run. ex: ``ls -lart /home``

    :param cwd: The directory from which to execute the command. Defaults
        to the home directory of the user specified by ``runas`` (or the user
        under which Salt is running if ``runas`` is not specified).

    :param stdin: A string of standard input can be specified for the
        command to be run using the ``stdin`` parameter. This can be useful in
        cases where sensitive information must be read from standard input.

    :param shell: If ``False``, let python handle the positional
        arguments. Set to ``True`` to use shell features, such as pipes or
        redirection.

    :param stdout:

    :param stderr:

    :param env: Environment variables to be set prior to execution.

        .. note::
            When passing environment variables on the CLI, they should be
            passed as the string representation of a dictionary.

            .. code-block:: bash

                idem exec cmd.run 'some command' env='{"FOO": "bar"}'
    :param umask: The umask (in octal) to use when running the command.

    :param timeout: A timeout in seconds for the executed process to return.

    CLI Example:

    .. code-block:: bash

        idem exec cmd.run "command" cwd=/home
    """
    ret = dict_tools.data.NamespaceDict()

    # Run the command
    if shell:
        proc = await asyncio.create_subprocess_shell(
            " ".join(cmd), cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
        )
    else:
        proc = await asyncio.create_subprocess_exec(
            *cmd, cwd=cwd, stdout=stdout, stderr=stderr, env=env, **kwargs
        )
    ret.pid = proc.pid

    # This is where the magic happens
    out, err = await asyncio.wait_for(proc.communicate(input=stdin), timeout=timeout)

    ret.stdout = (out or b"").decode()
    ret.stderr = (err or b"").decode()
    ret.retcode = await asyncio.wait_for(proc.wait(), timeout=timeout)
    return ret
