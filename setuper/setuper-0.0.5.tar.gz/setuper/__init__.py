import importlib.util
import setuptools
import shlex
import subprocess
import sys

def run(setup_path, pip_arguments="", remove_self=False, pip=[sys.executable, "-m", "pip"], extras=[]):
	pip_arguments = shlex.split(pip_arguments)
	def setuptools_setup(install_requires=[], extras_require={}, *args, **kwargs):
		requirements = []
		requirements += install_requires
		for extra in extras:
			if extra not in extras_require:
				raise SystemExit("No extra \"%s\" is known." % extra)
			requirements += extras_require[extra]
		subprocess.check_call(pip + ["install"] + requirements)
	setuptools.setup = setuptools_setup

	spec = importlib.util.spec_from_file_location("__main__", str(setup_path))
	setup = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(setup)

	if remove_self:
		subprocess.check_call(pip + ["uninstall", "--yes", "setuper"])
