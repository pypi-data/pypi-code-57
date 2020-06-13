from typing import Any, Dict, Tuple


def sig(hub, ctx, *args, **kwargs) -> Tuple[bool, Dict[str, Any]]:
    """
    All vultr functions require a ctx, that's all this sig enforces
    """


# TODO this needs to be a global contract, once that is working delete this from individual sub contracts
def post_list(hub, ctx):
    # Any list function should only show locations defined in this profile
    func_ctx = ctx.kwargs.get("ctx", ctx.args[1])
    DCID = func_ctx["acct"].get("DCID")

    if DCID is None or "DCID" in ctx.ret[1]:
        return ctx.ret
    else:
        ret = {}
        for key, value in ctx.ret[1].items():
            # Filter by DCID if it was part of the return
            if (
                not isinstance(value, dict)
                or "DCID" not in value
                or value["DCID"] == DCID
            ):
                ret[key] = value
        return ctx.ret[0], ret
