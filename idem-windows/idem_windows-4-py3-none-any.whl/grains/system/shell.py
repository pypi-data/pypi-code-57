import os


async def load_shell(hub):
    hub.grains.GRAINS.shell = os.environ.get("COMSPEC", r"C:\Windows\system32\cmd.exe")
