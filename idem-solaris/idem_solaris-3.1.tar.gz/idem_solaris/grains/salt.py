"""
TODO These grains are collected in salt, but some work regarding minion and master confs
needs to be done before they can be useful here
"""

import os


async def load_salt_path(hub):
    try:
        import salt

        hub.grains.GRAINS.saltpath = os.path.dirname(os.path.abspath(salt.__file__))
    except (ImportError, ModuleNotFoundError):
        hub.grains.GRAINS.saltpath = "unknown"


async def load_salt_version(hub):
    try:
        from salt.version import __version__, __version_info__

        hub.grains.GRAINS.saltversion = __version__
        hub.grains.GRAINS.saltversioninfo = __version_info__
    except (ImportError, ModuleNotFoundError):
        hub.grains.GRAINS.saltversion = "unknown"
        hub.grains.GRAINS.saltversioninfo = "unknown"
