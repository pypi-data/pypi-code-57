from typing import Any, Dict


def sig(hub, ctx, name: str, **kwargs) -> Dict[str, Dict[str, Any]]:
    pass


# TODO this needs to be a global contract for states
def call(hub, ctx):
    func_ctx = ctx.kwargs.get("ctx", None)
    if func_ctx:
        if not func_ctx["acct"]:
            raise ValueError("missing account information")
        elif not func_ctx["acct"].get("api_key"):
            raise ValueError("Incomplete account information: missing api_key")

    return ctx.func(*ctx.args, **ctx.kwargs)
