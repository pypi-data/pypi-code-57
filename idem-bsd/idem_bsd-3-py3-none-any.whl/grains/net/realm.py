import shutil


async def load_windows_domain(hub):
    if shutil.which("realm"):
        realms = (await hub.exec.cmd.run(["realm", "list", "--name-only"]))[
            "stdout"
        ].splitlines()
        if realms:
            hub.grains.GRAINS.windowsdomain = realms[0]
            hub.grains.GRAINS.windowsdomaintype = "Domain"
