import importlib.util
import sys
from os import path

import click

from nomnomdata.engine import logging as nomlogging
from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.core import Executable


@click.command()
@click.argument("executable", default="executable.py")
def run(executable):
    """ Run the target executable, expected to be a python file that contains a subclass of core.Executable"""
    nominode = NominodeClient()
    logger = nomlogging.getLogger("nomigen.run")
    spec = importlib.util.spec_from_file_location("executable", path.abspath(executable))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    executables = Executable.__subclasses__()
    if len(executables) != 1:
        logger.error(
            "Executable can only be subclassed once, current subclasses {}".format(
                executables
            )
        )
        sys.exit(1)
    else:
        executable = executables[0]
        with executable() as r:
            to_run = getattr(r, r.get_action())
            to_run()
        nominode.update_progress(progress=100)
