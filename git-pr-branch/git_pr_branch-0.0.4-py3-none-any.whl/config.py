import copy
import os
from collections.abc import MutableMapping

import attr
import toml


#: The default configuration settings. This should not be
#: modified and should be copied with :func:`copy.deepcopy`.
DEFAULTS = {
    "config_version": 1,
    "github_token": None,
    "upstream_remote": "origin",
    "verbose": False,
    "quiet": False,
}


def _check_not_none(config, key):
    if config[key] is None:
        raise ConfigurationException(f"you must set the {key} value")


#: The default validators for each configuration key.
VALIDATORS = {
    "github_token": _check_not_none,
}


@attr.s(auto_attribs=True)
class ConfigurationException:
    """
    Raised when there's an invalid configuration setting

    Args:
        message (str): A detailed description of the configuration problem
                       which is presented to the user.
    """

    message: str

    def __str__(self):
        return f"Configuration error: {self.message}"


@attr.s
class LazyConfig(MutableMapping):
    """This class lazy-loads the configuration file."""

    _app_name = attr.ib()
    _defaults = attr.ib(type=dict)
    _validators = attr.ib(type=dict, factory=dict)
    _data = attr.ib(init=False, factory=dict)
    loaded = attr.ib(init=False, default=False)
    _env_var = attr.ib(init=False)

    @_env_var.default
    def _default_env_var(self):
        return "{}_CONF".format(self._app_name.replace("-", "_").upper())

    @property
    def path(self):
        return os.path.expanduser("~/.config/{}/config.toml".format(self._app_name))

    def __getitem__(self, key):
        if not self.loaded:
            self.load()
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        if not self.loaded:
            self.load()
        return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        if not self.loaded:
            self.load()
        return self._data.__delitem__(key)

    def __iter__(self):
        if not self.loaded:
            self.load()
        return self._data.__iter__()

    def __len__(self):
        if not self.loaded:
            self.load()
        return self._data.__len__()

    def _validate(self):
        """Perform checks on the configuration to assert its validity.

        Raises:
            ConfigurationException: If the configuration is invalid.
        """
        for key in self:
            if key not in self._defaults:
                raise ConfigurationException(
                    'Unknown configuration key "{}"! Valid configuration keys are'
                    " {}".format(key, list(self._defaults.keys()))
                )
            if key in self._validators:
                self._validators[key](self, key)

    def _migrate(self):
        version = self.get("config_version", 1)
        # Do migrations here.
        if version == 1:
            pass

    def load(self, config_path=None):
        """Load application configuration from a file and merge it with the default configuration.

        If the appripriate environment variable is set to a filesystem path, the configuration will
        be loaded from that location.
        """
        self.loaded = True
        config = copy.deepcopy(self._defaults)

        if config_path is None and self._env_var in os.environ:
            config_path = os.environ[self._env_var]

        if config_path is None:
            config_path = self.path
        elif not os.path.exists(config_path):
            raise ConfigurationException(
                "the specified configuration file {} does not exist.".format(
                    config_path
                )
            )

        if os.path.exists(config_path):
            # _log.info("Loading configuration from {}".format(config_path))
            try:
                file_config = toml.load(config_path)
                for key in file_config:
                    config[key.lower()] = file_config[key]
            except toml.TomlDecodeError as e:
                msg = "Failed to parse {}: error at line {}, column {}: {}".format(
                    config_path, e.lineno, e.colno, e.msg
                )
                raise ConfigurationException(msg)

        self.update(config)
        self._migrate()
        self._validate()
        return self

    def write(self):
        conf_dir = os.path.dirname(self.path)
        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)
        with open(self.path, "w") as f:
            toml.dump(dict(self), f)

    def reset(self):
        self.loaded = False
        self._data = dict()


#: The configuration dictionary
conf = LazyConfig("git-pr-branch", defaults=DEFAULTS, validators=VALIDATORS)
