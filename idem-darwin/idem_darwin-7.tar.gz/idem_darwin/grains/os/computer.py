import shutil


async def load_computer_name(hub):
    scutil = shutil.which("scutil")
    if scutil:
        hub.grains.GRAINS.computer_name = (
            await hub.exec.cmd.run([scutil, "--get", "ComputerName"])
        ).stdout.strip()
