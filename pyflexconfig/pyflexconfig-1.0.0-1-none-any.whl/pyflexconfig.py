"""
============
pyflexconfig
============

A simple and flexible app configuration data provider.

Please read the README, the docstrings here, the tests and the ``demos/`` directory of the source bundle for more
documentation.
"""
import logging
import os
import pathlib
import runpy
import types
import typing

import pkg_resources

# Custom logger
LOG = logging.getLogger(name=__name__)

# PEP 396 style version marker
try:
    __version__ = pkg_resources.get_distribution("pyflexconfig").version
except pkg_resources.DistributionNotFound:
    LOG.warning("Could not get the package version from pkg_resources")
    __version__ = "unknown"

__author__ = "Gilles Lenfant"
__author_email__ = "gilles.lenfant@gmail.com"
__license__ = "MIT"

# Typing helpers

PathOrStr = typing.Union[str, pathlib.Path]


def pure_python_parser(source_path: PathOrStr) -> typing.Dict[str, typing.Any]:
    """Parses a Python file in a sandbox and provides its globals in a dict"""
    return runpy.run_path(source_path)


def keep_upper_names(config: types.SimpleNamespace) -> None:
    """Remove disallowed option names from a config object, the default ``filter_`` option of the ``bootstrap()`` main
    function.

    Args:
        config: The config object
    """

    def name_rejected(name: str) -> bool:
        """True if not an allowed option name.
        Legal names are:
        - All uppercases with potential "_" or [0..9] inside
        - Don't start with "_"
        """
        return name.startswith("_") or name.upper() != name

    # Remove "illegal" option names.
    for name in tuple(vars(config)):
        if name_rejected(name):
            delattr(config, name)


# These are Python automatic attribs we don't want whatever.
NAMES_BLACKLIST = ("__builtins__", "__cached__", "__doc__", "__file__", "__loader__", "__name__", "__package__",
                   "__spec__")


def bootstrap(
        config: types.SimpleNamespace,
        parser: typing.Callable = pure_python_parser,
        defaults_path: typing.Optional[PathOrStr] = None,
        custom_path: typing.Optional[PathOrStr] = None,
        custom_path_envvar: str = None,
        filter_: typing.Optional[typing.Callable] = keep_upper_names,
        validator: typing.Optional[typing.Callable] = None,
) -> None:
    """
    Bootstrap the configuration object populating the `config` namespace.

    Args:
        config: The global configuration namespace to populate, May bepre-populated.
        parser: (Optional) options file parser.
        defaults_path: (Optional) path to the default config file.
        custom_path: (Optional) path to a custom config file
        custom_path_envvar: (Optional) environment variable name that contains the config path.
        filter_: (Optional) options name filter callable that removes unwanted options.
                 Defaults to ``keep_upper_names```. See this function for required signature.
        validator: (Optional) validation callable that takes a config SimpleNamespace and
                   issues warnings or raises exceptions on invalid configuration options.
                   Note that the validator can change or add arbitrary options.

    Notes:

        If ``parser`` is provided, it must be a callable object that takes a file path object
        (of a configuration file) and returns a configuration dict whick keys are the option
        names. The default ``parser`` is the stdlib function ``runpy.run_path``

        If both ``custom_path`` and ``custom_path_envvar`` are provided, the second one is ignored.
        In both case the values from the custom config file replace the ones of same name from the
        default config file.
    """

    def blacklisted_removed(option: typing.Dict[str, typing.Any]) -> typing.Iterator[typing.Tuple[str, typing.Any]]:
        """Removes elements from blacklist"""
        return ((name, value) for name, value in option.items() if name not in NAMES_BLACKLIST)

    # Handling options provided by "default_path"
    if defaults_path:
        default_options = parser(defaults_path)
        for name, value in blacklisted_removed(default_options):
            setattr(config, name, value)

    # Handling custom options
    selected_conf_path = os.getenv(custom_path_envvar, None) if custom_path_envvar else None
    selected_conf_path = custom_path or selected_conf_path
    if selected_conf_path:
        selected_conf_path = pathlib.Path(selected_conf_path)
        if selected_conf_path.is_file():
            LOG.debug(f"Will load custom config file {selected_conf_path}")
            custom_options = parser(selected_conf_path)
            for name, value in blacklisted_removed(custom_options):
                setattr(config, name, value)
        else:
            LOG.error(f"Custom config file {selected_conf_path} does not exist. Ignoring it...")

    # Apply the potential ``filter_``
    if callable(filter_):
        filter_(config)

    # Validating the config if validator provided
    if callable(validator):
        validator(config)
