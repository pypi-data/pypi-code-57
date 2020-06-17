import cowsay.main as cow
import io
import shutil
import sys


async def _fortune(hub):
    cmd = shutil.which("fortune")
    if cmd:
        try:
            return (await hub.exec.cmd.run(cmd))["stdout"]
        except AttributeError:
            pass


async def load_fortune(hub):
    hub.grains.GRAINS.fortune = await _fortune(hub)


async def load_cowsay(hub):
    # Somewhere to store the output
    out = io.StringIO()
    # set stdout to our StringIO instance
    sys.stdout = out
    # Print out the cowsay command
    cow.cow(await _fortune(hub) or "There is no cow level")
    # Restore stdout
    sys.stdout = sys.__stdout__
    # return the stored value from previous print
    hub.grains.GRAINS.cowsay = out.getvalue()
