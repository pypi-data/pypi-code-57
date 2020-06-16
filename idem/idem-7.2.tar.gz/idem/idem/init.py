# The order of the sequence that needs to be implemented:
# Start with a single sls file, just like you started with salt
# Stub out the routines around gathering the initial sls file
# Just use a yaml renderer and get it to where we can manage some basic
# includes to drive to highdata

# Then we can start to fill out renderers while at the same time
# deepening the compiler

# Import python libs
import asyncio
import os
import copy


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.idem, recurse=True)
    hub.idem.RUNS = {}
    hub.pop.sub.add(dyne_name="log")
    hub.pop.sub.add(dyne_name="acct")
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.load_subdirs(hub.exec, recurse=True)
    hub.pop.sub.add(dyne_name="states")
    hub.pop.sub.load_subdirs(hub.states, recurse=True)
    hub.idem.req.init.req_map()


def cli(hub):
    """
    Execute a single idem run from the cli
    """
    hub.pop.config.load(["idem", "acct"], cli="idem")
    hub.pop.loop.start(hub.idem.init.cli_apply())


# If the gathering and cli def funcs grow they should be moved to a plugin
def get_refs(hub):
    """
    Determine where the sls sources are
    """
    sls_sources = []
    slses = []
    for sls in hub.OPT["idem"]["sls"]:
        if os.path.isfile(sls):
            if sls.endswith(".sls"):
                ref = sls[:-4]
            else:
                ref = sls
            slses.append(ref)
            sls_dir = os.path.dirname(sls)
            implied = f"file://{sls_dir}"
            if implied not in sls_sources:
                sls_sources.append(implied)
        else:
            slses.append(sls)
    if hub.OPT["idem"]["tree"]:
        tree = f"file://{hub.OPT['idem']['tree']}"
        if tree not in sls_sources:
            sls_sources.insert(0, tree)
    sls_sources.extend(hub.OPT["idem"]["sls_sources"])
    return {"sls_sources": sls_sources, "sls": slses}


async def cli_apply(hub):
    """
    Run the CLI routine in a loop
    """
    if hub.SUBPARSER == "state":
        await hub.idem.init.cli_sls()
    elif hub.SUBPARSER == "exec":
        await hub.idem.init.cli_exec()


async def cli_sls(hub):
    """
    Execute the cli routine to run states
    """
    src = hub.idem.init.get_refs()
    await hub.idem.state.apply(
        "cli",
        src["sls_sources"],
        hub.OPT["idem"]["render"],
        hub.OPT["idem"]["runtime"],
        ["states"],
        hub.OPT["idem"]["cache_dir"],
        src["sls"],
        hub.OPT["idem"]["test"],
        hub.OPT["acct"]["acct_file"],
        hub.OPT["acct"]["acct_key"],
        hub.OPT["acct"]["acct_profile"],
    )

    errors = hub.idem.RUNS["cli"]["errors"]
    if errors:
        display = getattr(hub, "output.nested.display")(errors)
        print(display)
        return
    running = hub.idem.RUNS["cli"]["running"]
    output = hub.OPT["idem"]["output"]
    display = getattr(hub, f"output.{output}.display")(running)
    print(display)


async def cli_exec(hub):
    exec_path = hub.OPT.idem.exec_func
    exec_args = hub.OPT.idem.exec_args
    if not exec_path.startswith("exec"):
        exec_path = f"exec.{exec_path}"
    args = []
    kwargs = {}
    for arg in exec_args:
        if isinstance(arg, dict):
            kwargs.update(arg)
        else:
            args.append(arg)
    try:
        ret = await hub.idem.ex.run(
            exec_path,
            args,
            kwargs,
            hub.OPT.acct.acct_file,
            hub.OPT.acct.acct_key,
            hub.OPT.acct.acct_profile,
        )
    except AttributeError:
        print(f"The desired execution is not available: {exec_path}")
        return
    output = hub.OPT.idem.output
    # exec can't use the idem outputter
    # TODO in pop-config allow subcommands to have different defaults from their parent
    if output == "idem":
        output = "nested"
    display = getattr(hub, f"output.{output}.display")(ret)
    print(display)
