import os


async def load_shell(hub):
    hub.grains.GRAINS.shell = os.environ.get("SHELL", "/bin/sh")
