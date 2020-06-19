import os
import pwd


async def load_console_user(hub):
    """
    Gets the Username of the current logged in console user.
    """
    console = "/dev/console"
    if os.path.exists(console):
        # returns the 'st_uid' stat from the /dev/console file.
        uid = os.stat(console)[4]
        hub.grains.GRAINS.console_user = uid
    else:
        hub.grains.GRAINS.console_user = 0
    hub.grains.GRAINS.console_username = pwd.getpwuid(
        hub.grains.GRAINS.console_user
    ).pw_name
