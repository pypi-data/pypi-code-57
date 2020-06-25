__version__ = "2020.6.0"
__banner__ = f"""
                     __                           __
                    |  |_.----.-----.-----.----. |__.-----.
                    |   _|   _|  _  |  _  |   ___|  |  _  |
                    |____|__| |___  |___  |__||__|__|_____|
                              |_____|_____|

                    version {__version__}
                    please, be patient ... :)


"""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ("__version__", "__banner__")
