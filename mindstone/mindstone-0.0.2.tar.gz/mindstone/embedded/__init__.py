""" embedded agent systems sub-package.

"""

from mindstone.embedded.driver import Driver

__all__ = ["Driver", "start_driver"]


def start_driver(platform: str, *args, **kwargs):
    if platform == "virtual":
        from mindstone.embedded.platforms.virtual import VirtualPlatform
        VirtualPlatform()
    elif platform == "raspberry":
        from mindstone.embedded.platforms.raspberry import RPiPlatform
        RPiPlatform()
    else:
        raise Exception("Invalid platform provided.")

    driver = Driver()
    driver.start(*args, **kwargs)
