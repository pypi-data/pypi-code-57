import importlib.util
import setuptools
import shlex
import subprocess
import sys

def run(setup_path, pip_arguments="", remove_self=False, pip=[sys.executable, "-m", "pip"]):
	pip_arguments = shlex.split(pip_arguments)
	def setuptools_setup(install_requires=[], *args, **kwargs):
		requirements = []
		requirements += install_requires
		subprocess.check_call(pip + ["install"] + requirements)
	setuptools.setup = setuptools_setup

	spec = importlib.util.spec_from_file_location("__main__", str(setup_path))
	setup = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(setup)

	if remove_self:
		subprocess.check_call(pip + ["uninstall", "--yes", "setuper"])
