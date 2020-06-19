import json
import shlex
from typing import Any, Dict

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


def post_run(hub, ctx):
    kwargs = ctx.get_arguments()
    if kwargs["stateful"]:
        return _reinterpreted_state(hub, ctx.ret)
    else:
        return ctx.ret
