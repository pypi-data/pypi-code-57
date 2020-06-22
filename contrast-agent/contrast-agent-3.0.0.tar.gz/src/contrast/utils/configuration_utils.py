# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import distutils.util
import os

from contrast.extern.ruamel import yaml

from contrast.api.settings_pb2 import ProtectionRule

import logging

logger = logging.getLogger("contrast")


CONFIG_LOCATIONS = [
    os.path.join(os.getcwd(), "settings"),
    os.getcwd(),
    "/etc/contrast/python",
    "/etc/contrast/",
]

CONFIG_FILE_NAMES = ["contrast_security.yaml", "contrast_security.yml"]


def load_yaml_config():
    """
    Checks for a yaml file at preconfigured file system location.

    See official documentation because this is valid across agents.

    Current order of precedence:
        CONTRAST_CONFIG_PATH env var
        os.path.join(os.getcwd(), 'settings')
        os.getcwd()
        /etc/contrast/python/
        /etc/contrast/
    :return: a dict object representation of the yaml config. {'enable': True, ....}
    """
    locations = CONFIG_LOCATIONS
    names = CONFIG_FILE_NAMES

    if "CONTRAST_CONFIG_PATH" in os.environ:
        locations = [os.environ.get("CONTRAST_CONFIG_PATH")] + locations

    config = None
    for path in locations:
        for name in names:
            file_path = os.path.join(path, name)

            if not os.path.exists(file_path):
                continue

            with open(file_path, "r") as config_file:
                logger.info(
                    "Loading configuration file: %s", os.path.abspath(file_path)
                )

                config = yaml.safe_load(config_file)

            if config:
                return config
    return config


def flatten_config(config):
    """
    Convert a nested dict such as
        {'enable': True,
        'application':
            {'name': 'dani-flask'},
        'agent':
            {'python':
                {'enable_rep': True}...

    into
        {'enable': True,
        'application.name': 'dani-flask',
        'agent.python.enable_rep': True,

    :param config: dict config with nested keys and values
    :return: dict, flattened where each key has one value.
    """
    flattened_config = {}

    def flatten(x, name=""):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], name + key + ".")
        else:
            flattened_config[name[:-1]] = x

    flatten(config)
    return flattened_config


def str_to_bool(val):
    """
    Converts a str to a bool

    true -> True, false -> False
    """
    if isinstance(val, bool):
        return val

    if val is None:
        return False

    return bool(distutils.util.strtobool(val))


def get_env_key(key):
    return os.environ.get(key)


def parse_disabled_rules(disabled_rules):
    if not disabled_rules:
        return []

    return [rule.lower() for rule in disabled_rules.split(",")]


PROTOBUF_MODES = {
    "monitor": ProtectionRule.MONITOR,
    "block": ProtectionRule.BLOCK,
    "block_at_perimeter": ProtectionRule.BLOCK_AT_PERIMETER,
    "off": ProtectionRule.NO_ACTION,
}


def protect_mode_to_protobuf(mode):
    """
    Converts str mode to protobuf friendly mode
    """
    if not mode:
        return ProtectionRule.NO_ACTION

    return PROTOBUF_MODES.get(mode.lower(), ProtectionRule.MONITOR)
