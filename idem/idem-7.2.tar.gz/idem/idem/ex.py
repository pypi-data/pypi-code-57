# Import python libs
import asyncio


async def run(
    hub, path, args, kwargs, acct_file=None, acct_key=None, acct_profile="default"
):
    ctx = {}
    if not path.startswith("exec."):
        path = f"exec.{path}"
    if acct_file and acct_key:
        first = path[path.index(".") + 1 :]
        sname = first[: first.index(".")]
        acct_paths = (f"exec.{sname}.ACCT", f"states.{sname}.ACCT")
        subs = []
        for name in acct_paths:
            if hasattr(hub, name):
                subs = getattr(hub, name)
        ctx["acct"] = hub.acct.init.unlock(acct_file, acct_key)
        ctx["acct"] = await hub.acct.init.gather(subs, acct_profile)
    func = getattr(hub, path)
    params = func.signature.parameters
    if "ctx" in params:
        args.insert(0, ctx)
    ret = func(*args, **kwargs)
    if asyncio.iscoroutine(ret):
        ret = await ret
    return ret
