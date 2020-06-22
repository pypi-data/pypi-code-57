#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations, unicode_literals
import os
import sys
import subprocess
import argparse
from shutil import rmtree
from setuptools import Command, find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install
from distutils.command.clean import clean


PROTO_PATH = os.path.join(os.curdir, "protos")
PYTHON_PATH = os.curdir
BUILD_PATH = os.path.join(os.curdir, "build")
DIST_PATH = os.path.join(os.curdir, "dist")
EGG_INFO_PATH = os.path.join(os.curdir, "willowlabs.egg-info")
EGGS_PATH = os.path.join(os.curdir, ".eggs")


if sys.version_info < (3, 7):
    sys.stderr.write("willowlabs-apis-python requires python3 version >= 3.7.0")
    sys.exit(-1)


def argparser():
    parser = argparse.ArgumentParser()
    parser.usage = "Usage: [PYTHON_COMMAND] setup.py [ACTION] [OPTIONS]\nFor example, python setup.py build --protoc " \
                   "/usr/local/bin/protoc"
    help_text = "The action that setup is to perform. Supported actions are build, install, clean, bdist_wheel, etc."
    parser.add_argument("action", help=help_text, type=str)
    default_compiler = "python -m grpc_tools.protoc"
    help_text = f"(Optional) The command to compile the the .proto files, e.g. protoc.exe. The command must be in " \
                f"quotes if the command contains a space. The default value is '{default_compiler}' and would " \
                f"require the Python3 packages 'grpcio' and 'grpcio-tools' to be installed."
    parser.add_argument("-pc", "--protoc", help=help_text, default=default_compiler, dest="protoc")
    return parser


class CompileGRPC(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        proto_files = [os.path.join(directory, filename) for directory, _, files in os.walk(PROTO_PATH)
                       for filename in files if filename.endswith(".proto")]
        command = " ".join([args.protoc, f"--proto_path={PROTO_PATH}", f"--python_out={PYTHON_PATH}",
                            f"--grpc_python_out={PYTHON_PATH}"] + proto_files)
        if subprocess.run(command, shell=True).returncode:
            sys.stderr.write("There has been an error compiling .proto files. Exiting.")
            sys.exit(-1)
        return None


class BuildPyCommand(build_py):
    def run(self):
        self.run_command("compile_grpc")
        build_py.run(self)


class InstallCommand(install):
    def run(self):
        self.run_command("compile_grpc")
        install.run(self)


class CleanPyCommand(clean):
    def run(self):
        for path in [BUILD_PATH, DIST_PATH, EGG_INFO_PATH, EGGS_PATH]:
            if os.path.exists(path):
                rmtree(path)

        for directory, _, filenames in os.walk(os.path.join(PYTHON_PATH, "willowlabs")):
            for filename in filenames:
                if filename.endswith("_pb2.py") or filename.endswith("_pb2_grpc.py"):
                    os.remove(os.path.join(directory, filename))

        for path in [os.path.join(PYTHON_PATH, "build"), os.path.join(PYTHON_PATH, "dist"),
                     os.path.join(PYTHON_PATH, ".eggs"), os.path.join(PYTHON_PATH, "willowlabs.egg-info")]:
            if os.path.exists(path):
                rmtree(path)
        clean.run(self)


def get_long_description() -> str:
    with open("README.rst", "r") as readme:
        long_description = readme.read()
    return long_description


def get_version() -> str:
    with open(os.path.join(os.curdir, "willowlabs", "__init__.py"), "r") as file:
        exec(file.read(), globals())
        global __version__
    return __version__


install_requires = ["google-api-python-client>=1.7.11", "grpcio>=1.27.0", "grpcio-tools>=1.27.2", "PyYAML>=5.3"]

if __name__ == "__main__":
    args = argparser().parse_args()
    setup(
        cmdclass={"compile_grpc": CompileGRPC, "build_py": BuildPyCommand, "clean": CleanPyCommand},
        name="willowlabs",
        namespace_packages=["willowlabs"],
        version=get_version(),
        author="Willow Labs AS",
        author_email="lars@willowlabs.ai",
        description="A Python package for accessing the Willow Labs APIs",
        long_description=get_long_description(),
        long_description_content_type="text/x-rst",
        license='MIT',
        url="https://github.com/willowlabs/willowlabs-apis-python",
        python_requires=">=3.7.0",
        install_requires=install_requires,
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Internet :: WWW/HTTP"
        ]
    )
