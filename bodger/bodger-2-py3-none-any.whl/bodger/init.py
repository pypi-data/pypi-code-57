# Import python libs
import asyncio
import fnmatch
import sys


def __init__(hub):
    # Remember not to start your app in the __init__ function
    # This function should just be used to set up the plugin subsystem
    # Add another function to call from your run.py to start the app
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.add(dyne_name="grains")


def cli(hub):
    hub.pop.config.load(["bodger", "grains"], cli="bodger")
    hub.grains.init.standalone()
    hub.pop.loop.start(hub.bodger.init.match())


async def match(hub):
    """
    Find the command to execute in the config, match the grains data and run
    """
    runs = []
    cmd = hub.OPT.bodger.cmd
    if cmd not in hub.OPT.bodger:
        hub.log.error(f"Command {cmd} not found!")
        return
    for tgt in hub.OPT.bodger[cmd]:
        grain, glob = tgt.split(":")
        val = hub.grains.GRAINS.get(grain)
        if fnmatch.fnmatch(val, glob):
            tcmd = hub.OPT.bodger[cmd][tgt]
            if isinstance(tcmd, str):
                runs.append(tcmd)
            else:
                runs.extend(tcmd)

    for run in runs:
        ret = await hub.exec.cmd.run(run, shell=True, stdout=sys.stdout.buffer)
        if ret.retcode != 0:
            # Stop on the first command that fails
            raise OSError(
                f"Command '{run}' executed by bodger exited with a bad return code '{ret.retcode}': {ret.stderr}"
            )
