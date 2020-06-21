"""
1. Put you code into script/__main__.py
2. List any dependencies in script/requirements.txt (Optional)
3. Run "pythere user@remotehost script/"

Pythere bundles any files in the script folder and execute on remote host.
If script/requirements.txt exists, the listed dependencies will
be available. (Only pure python packages will be guaranteed to work)
"""

import argparse
import fabric
import zipapp
import shutil
import subprocess
import sys
import getpass
from pathlib import Path


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("remotehost", help="target machine to connect to")
	parser.add_argument("script", help="python file/folder to run remotely")
	parser.add_argument("--requirements", "-r", help="Requirements to bundle with script")
	parser.add_argument("target_args", nargs=argparse.REMAINDER,
	    help="arguments to pass to script.py when executing on the remotehost.")

	args = parser.parse_args()
	script_dir = Path(args.script)
	assert script_dir.is_dir()

	build_dir = Path.cwd() / "build"
	executable = script_dir.with_suffix(".pyz")
	
	clean(build_dir)
	prepare(build_dir, script_dir, args.requirements)
	build(build_dir, executable)
	copy_and_run(executable, args.remotehost)


def clean(build_dir):
	if build_dir.exists():
		shutil.rmtree(build_dir)


def prepare(build_dir, script_dir, requirements):
	shutil.copytree(script_dir, build_dir)

	pip_args = [sys.executable, "-m", "pip", "install", "--target", build_dir]

	if requirements:
		pip_args.append("-r")
		pip_args.append(args.requirements)
		subprocess.run(pip_args)
	else:
		requirements_path = script_dir / "requirements.txt"
		if requirements_path.exists():
			pip_args.append("-r")
			pip_args.append(str(requirements_path))
			subprocess.run(pip_args)


def build(build_dir, executable):
	zipapp.create_archive(build_dir, target=executable)


def copy_and_run(executable, remotehost):
	user, host = remotehost.split("@")
	print(user, host)
	pw = getpass.getpass(f"Enter password for {remotehost}:")
	connect_kwargs = {
	"password": pw,
	}

	remote = fabric.Connection(host, user, connect_kwargs=connect_kwargs)
	with remote:
		remote.put(executable, "pythere_target.pyz")
		remote.run("python pythere_target.pyz", pty=True)


if __name__ == "__main__":
	main()
