import os
import sys


async def load_cwd(hub):
    """
    Current working directory
    """
    hub.grains.GRAINS.cwd = os.getcwd()


async def load_path(hub):
    """
    Return the path
    """
    # Provides:
    #   path
    hub.grains.GRAINS.path = os.environ.get("PATH", "")


async def load_pythonpath(hub):
    """
    Return the Python path
    """
    # Provides:
    #   pythonpath
    hub.grains.GRAINS.pythonpath = sorted((str(p) for p in sys.path), key=str.casefold)


async def load_executable(hub):
    """
    Return the python executable in use
    """
    # Provides:
    #   pythonexecutable
    hub.grains.GRAINS.pythonexecutable = sys.executable


async def load_shell(hub):
    hub.grains.GRAINS.shell = os.environ.get("SHELL", "/bin/sh")
