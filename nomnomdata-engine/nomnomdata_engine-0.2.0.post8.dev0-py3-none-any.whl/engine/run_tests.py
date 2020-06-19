import importlib.util
import json
import os
import subprocess
import sys
from os import path

import click
import pytest

from nomnomdata.engine.core import Executable
from nomnomdata.engine.test import NominodeMock


def clear_pycache():
    subprocess.check_call("find . -name '*.pyc' -delete", shell=True)


@click.command(name="run_tests")
@click.option(
    "-t", "--test", help="Run a specific test name (equivalent to pytest -k option)"
)
@click.option(
    "-c",
    "--creds_dir",
    default="/nomnom/test_config",
    show_default=True,
    envvar="NOMIGEN_TEST_CREDENTIALS",
    help="Credentials folder, will try environment variable NOMIGEN_TEST_CREDENTIALS, before falling back to default",
)
@click.pass_context
def run_tests(ctx, creds_dir=None, test=None):
    """Run engine tests with pytest, checks NOMIGEN_TEST_CREDENTIALS environment variable for creds location, otherwise uses /nomnom/test_config"""
    clear_pycache()
    old_environ = os.environ.copy()
    try:
        os.environ["log_level"] = ctx.obj["LOG_LEVEL"]
        xml_dest = os.path.join(creds_dir, "test-reports", "nomtest.xml")
        pytestargs = ["-s", "-v", "--cache-clear", "--junitxml={}".format(xml_dest)]
        if test:
            pytestargs.extend(["-k", test])
        pytestargs.extend(["--cov-fail-under=80", "--cov=pkg"])
        result = pytest.main(pytestargs)
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
    sys.exit(result)


@click.command()
@click.option(
    "-p",
    "--parameter_file",
    default="params.json",
    show_default=True,
    help="Parameter JSON file to use",
)
@click.argument("action_name")
@click.argument("executable", default="executable.py")
@click.pass_context
def run_mock(ctx, action_name, executable, parameter_file):
    """Run the target executable, expected to be a python file that contains a subclass of core.Executable"""
    clear_pycache()
    old_environ = os.environ.copy()
    try:
        with open(parameter_file, "r") as pfile:
            params = json.load(pfile)
        os.environ["log_level"] = ctx.obj["LOG_LEVEL"]
        spec = importlib.util.spec_from_file_location(
            "executable", path.abspath(executable)
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        executables = Executable.__subclasses__()
        with NominodeMock(params):
            executable = executables[0]
            with executable() as r:
                to_run = getattr(r, action_name)
                to_run()
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
