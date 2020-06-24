# -*- coding: utf-8 -*-
import operator
import os
from functools import reduce

import configparser
from pybuilder.core import init

__author__ = u"Martin Grůber"

try:
    string_types = basestring
except NameError:
    string_types = str


def read_from(filename):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)) as f:
        result = f.read()
    return result


@init
def init_setup_cfg_plugin(project, logger):
    pass


@init
def init1_from_setup_cfg(project):

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read("setup.cfg")

    name = os.environ.get("PYB_SCFG_NAME", config.get("metadata", "name", fallback=None))
    version = os.environ.get("PYB_SCFG_VERSION", config.get("metadata", "version", fallback=None))
    if version and version.startswith("file: "):
        version = read_from(version.split(maxsplit=1)[1])
    distutils_commands = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DISTUTILS_COMMANDS", config.get("tool:pybuilder", "distutils_commands", fallback="sdist")
        ).split()
    )))
    distutils_upload_repository = os.environ.get(
        "PYB_SCFG_UPLOAD_REPOSITORY", config.get("tool:pybuilder", "distutils_upload_repository", fallback=None)
    )
    copy_resources_glob = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "copy_resources_glob", fallback="").split()
    )))
    package_data = dict(map(
        lambda t: (t[0].strip(), t[1].strip().split()),
        [
            line.strip().split("=", maxsplit=1)
            for line in config.get("files", "package_data", fallback="").splitlines()
            if line.strip()
        ]
    ))
    cython_include_modules = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "cython_include_modules", fallback="").split()
    )))
    cython_exclude_modules = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), config.get("tool:pybuilder", "cython_exclude_modules", fallback="").split()
    )))
    cython_remove_python_sources = config.getboolean(
        "tool:pybuilder", "cython_remove_python_sources", fallback=False
    )
    pytest_coverage_break_build_threshold = os.environ.get(
        "PYB_SCFG_PYTEST_COVERAGE_BREAK_BUILD_THRESHOLD",
        config.get("tool:pytest", "coverage_break_build_threshold", fallback=None)
    )

    # analyze - Python flake8 linting
    # publish - create distributions (sdist, bdist)
    # upload - upload to the PyPI server
    # clean - clean all temporary files
    # sphinx_generate_documentation - generate sphinx documentation
    default_task = list(filter(lambda item: item.strip(), map(
        lambda item: item.strip(), os.environ.get(
            "PYB_SCFG_DEFAULT_TASK", config.get("tool:pybuilder", "default_task", fallback="analyze publish clean")
        ).split()
    )))

    if name:
        project.set_property("name", name)
        # Setting property is not enough
        project.name = name

    if version:
        project.set_property("version", version)
        # Setting property is not enough
        project.version = project.get_property("version")

    if default_task:
        # Setting property is breaking this thing...
        # project.set_property("default_task", default_task)
        project.default_task = default_task

    if distutils_commands:
        project.set_property("distutils_commands", distutils_commands)

    # TWINE_REPOSITORY_URL environment variable is preferred
    if os.environ.get("TWINE_REPOSITORY_URL") is None and distutils_upload_repository is not None:
        project.set_property("distutils_upload_repository", distutils_upload_repository)

    if len(cython_include_modules):
        # Cython extension modules definition
        project.set_property("distutils_cython_ext_modules", [{
            "module_list": cython_include_modules,
            "exclude": cython_exclude_modules,
        }])

    if cython_remove_python_sources:
        # Remove the original Python source files from the distribution
        project.set_property("distutils_cython_remove_python_sources", cython_remove_python_sources)

    if copy_resources_glob:
        project.set_property("copy_resources_glob", copy_resources_glob + reduce(operator.concat, package_data.values(), []))

    if package_data:
        # The files pattern MUST NOT contain the package name and MUST use '/' as a path separator
        project.package_data.update({k: ["/".join(i.split("/")[1:]) for i in v] for k, v in package_data.items()})

    try:
        pytest_coverage_break_build_threshold = int(pytest_coverage_break_build_threshold)
    except (ValueError, TypeError):
        pytest_coverage_break_build_threshold = None
    if pytest_coverage_break_build_threshold is not None:
        project.set_property("pytest_coverage_break_build_threshold", pytest_coverage_break_build_threshold)
