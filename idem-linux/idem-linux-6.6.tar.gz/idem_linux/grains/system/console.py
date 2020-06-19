import getpass
import pwd


async def load_console_user(hub):
    hub.grains.GRAINS.console_username = getpass.getuser()
    hub.grains.GRAINS.console_user = pwd.getpwnam(
        hub.grains.GRAINS.console_username
    ).pw_uid
