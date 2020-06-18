import copy
import os
from typing import Any, Dict, List

__virtualname__ = "cmd"


def __virtual__(hub):
    hub.log.debug("cmd state is a work in progress")
    return False


async def run(
    hub,
    ctx,
    name: str or List[str],
    cwd: str = None,
    shell: bool = False,
    env: Dict[str, Any] = None,
    umask: str = None,
    timeout: int or float = None,
    ignore_timeout: bool = False,
    stateful: bool = False,
    **kwargs,
) -> Dict[str, Any]:
    """
    Run a command if certain circumstances are met.  Use ``cmd.wait`` if you
    want to use the ``watch`` requisite.

    name
        The command to execute, remember that the command will execute with the
        path and permissions of the salt-minion.

    cwd
        The current working directory to execute the command in, defaults to
        /root

    shell
        run the command with default shell

    stateful
        The command being executed is expected to return data about executing
        a state. For more information, see the :ref:`stateful-argument` section.

    umask
        The umask (in octal) to use when running the command.

    timeout
        If the command has not terminated after timeout seconds, send the
        subprocess sigterm, and if sigterm is ignored, follow up with sigkill

    ignore_timeout
        Ignore the timeout of commands, which is useful for running nohup
        processes.
    """
    ### NOTE: The keyword arguments in **kwargs are passed directly to the
    ###       ``cmd.run`` function and cannot be removed from the function
    ###       definition, otherwise the use of unsupported arguments in a
    ###       ``cmd.run`` state will result in a traceback.

    ret = {"name": name, "changes": {}, "result": False, "comment": ""}
    test_name = None
    if isinstance(stateful, list) and "test_name" in stateful[0]:
        test_name = stateful[0]["test_name"]
    if ctx["test"] and test_name:
        name = test_name

    # Need the check for None here, if env is not provided then it falls back
    # to None and it is assumed that the environment is not being overridden.
    if env is not None and not isinstance(env, (list, dict)):
        ret["comment"] = "Invalidly-formatted 'env' parameter. See " "documentation."
        return ret

    cmd_kwargs = copy.deepcopy(kwargs)
    cmd_kwargs.update(
        {
            "cwd": cwd,
            "shell": shell if hasattr(hub, "grains") else "sh",
            "env": env,
            "umask": umask,
        }
    )

    if ctx["test"] and not test_name:
        ret["result"] = None
        ret["comment"] = 'Command "{0}" would have been executed'.format(name)
        return ret

    if cwd and not os.path.isdir(cwd):
        ret["comment"] = f'Desired working directory "{cwd}" ' "is not available"
        return ret

    # Wow, we passed the test, run this sucker!
    try:
        cmd_all = await hub.exec.cmd.run(
            cmd=name, timeout=timeout, python_shell=True, **cmd_kwargs
        )
    except Exception as err:  # pylint: disable=broad-except
        ret["comment"] = str(err)
        return ret

    ret["changes"] = cmd_all
    ret["result"] = not bool(cmd_all.retcode)
    ret["comment"] = f'Command "{name}" run'

    # Ignore timeout errors if asked (for nohups) and treat cmd as a success
    if ignore_timeout:
        trigger = "Timed out after"
        if ret["changes"].get("retcode") == 1 and trigger in ret["changes"].get(
            "stdout"
        ):
            ret["changes"]["retcode"] = 0
            ret["result"] = True

    if ctx["test"] and cmd_all["retcode"] == 0 and ret["changes"]:
        ret["result"] = None

    return ret
