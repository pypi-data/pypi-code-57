import copy
import json
import os
import shlex
from typing import Any, Dict, List

__virtualname__ = "cmd"


def _is_true(hub, val: str) -> bool:
    if val and str(val).lower() in ("true", "yes", "1"):
        return True
    elif str(val).lower() in ("false", "no", "0"):
        return False
    raise ValueError(f"Failed parsing boolean value: {val}")


def _failout(hub, state: Dict[str, Any], msg: str) -> Dict[str, Any]:
    state["comment"] = msg
    state["result"] = False
    return state


def _reinterpreted_state(hub, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Re-interpret the state returned by salt.state.run using our protocol.
    """
    ret = state["changes"]
    state["changes"] = {}
    state["comment"] = ""

    out = ret.get("stdout")
    if not out:
        if ret.get("stderr"):
            state["comment"] = ret["stderr"]
        return state

    is_json = False
    try:
        data = json.loads(out)
        if not isinstance(data, dict):
            return _failout(
                hub, state, "script JSON output must be a JSON object (e.g., {})!"
            )
        is_json = True
    except ValueError:
        idx = out.rstrip().rfind("\n")
        if idx != -1:
            out = out[idx + 1 :]
        data = {}
        try:
            for item in shlex.split(out):
                key, val = item.split("=")
                data[key] = val
        except ValueError:
            state = _failout(
                state,
                "Failed parsing script output! "
                "Stdout must be JSON or a line of name=value pairs.",
            )
            state["changes"].update(ret)
            return state

    changed = _is_true(hub, data.get("changed", "no"))

    if "comment" in data:
        state["comment"] = data["comment"]
        del data["comment"]

    if changed:
        for key in ret:
            data.setdefault(key, ret[key])

        # if stdout is the state output in JSON, don't show it.
        # otherwise it contains the one line name=value pairs, strip it.
        data["stdout"] = "" if is_json else data.get("stdout", "")[:idx]
        state["changes"] = data

    # FIXME: if it's not changed but there's stdout and/or stderr then those
    #       won't be shown as the function output. (though, they will be shown
    #       inside INFO logs).
    return state


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
        The shell to use for execution, defaults to the shell grain

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
    if not isinstance(stateful, list):
        stateful = stateful is True
    elif isinstance(stateful, list) and "test_name" in stateful[0]:
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
            "shell": shell or hub.grains.GRAINS.get("shell", "sh")
            if hasattr(hub, "grains")
            else "sh",
            "env": env,
            "umask": umask,
        }
    )

    if ctx["test"] and not test_name:
        ret["result"] = None
        ret["comment"] = 'Command "{0}" would have been executed'.format(name)
        return _reinterpreted_state(hub, ret) if stateful else ret

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

    if stateful:
        ret = _reinterpreted_state(hub, ret)
    if ctx["test"] and cmd_all["retcode"] == 0 and ret["changes"]:
        ret["result"] = None
    return ret
