# Import python libs
import asyncio

__func_alias__ = {"compile_": "compile"}


def create(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    subs,
    cache_dir,
    test,
    acct_file,
    acct_key,
    acct_profile,
):
    """
    Create a new instance to execute against
    """
    hub.idem.RUNS[name] = {
        "sls_sources": sls_sources,
        "render": render,
        "runtime": runtime,
        "subs": subs,
        "cache_dir": cache_dir,
        "states": {},
        "test": test,
        "resolved": set(),
        "files": set(),
        "high": {},
        "post_low": [],
        "errors": [],
        "iorder": 100000,
        "sls_refs": {},
        "blocks": {},
        "running": {},
        "run_num": 1,
        "add_low": [],
        "acct_profile": acct_profile,
    }
    if acct_file and acct_key:
        hub.idem.RUNS[name]["acct"] = hub.acct.init.unlock(acct_file, acct_key)


async def apply(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    subs,
    cache_dir,
    sls,
    test=False,
    acct_file=None,
    acct_key=None,
    acct_profile="default",
):
    """
    Run idem!
    """
    hub.idem.state.create(
        name,
        sls_sources,
        render,
        runtime,
        subs,
        cache_dir,
        test,
        acct_file,
        acct_key,
        acct_profile,
    )
    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using act/idem
    await hub.idem.resolve.gather(name, *sls)
    if hub.idem.RUNS[name]["errors"]:
        return
    await hub.idem.state.compile(name)
    if hub.idem.RUNS[name]["errors"]:
        return
    ret = await hub.idem.run.init.start(name)


async def compile_(hub, name):
    """
    Compile the data defined in the given run name
    """
    for mod in hub.idem.compiler:
        if hasattr(mod, "stage"):
            ret = mod.stage(name)
            if asyncio.iscoroutine(ret):
                await ret
