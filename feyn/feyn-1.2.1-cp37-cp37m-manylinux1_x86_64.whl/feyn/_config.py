import logging
import os
import warnings
from configparser import ConfigParser
from pathlib import Path

resolve_config_failed_message = """Could not resolve `url` and `api_token` from environment variables or configuration file.
Please either set the environment variables [FEYN_QLATTICE_URL] and [FEYN_QLATTICE_API_TOKEN].
Or put a configuration file named [.feynrc] or [feyn.ini] in your home folder."""

_config_file_paths = [
    Path.home().joinpath(".feynrc"),
    Path.home().joinpath("feyn.ini"),
]

class Config:
    def __init__(self, url, api_token):
        self.url = url
        self.api_token = api_token


def resolve_config(section=None) -> Config:
    if section:
        config_file = _find_config_file()

        if config_file is None:
            raise FileNotFoundError(f"Configuration file not found. Searched: {[str(x) for x in _config_file_paths]}.")

        return _load_from_ini_file(config_file, section)

    # Use env vars if no section specified
    config = _try_load_from_environment_vars()
    if config:
        return config

    # Fall back to first section in a config file
    config_file = _find_config_file()
    if config_file:
        first_section = _get_first_section(config_file)
        return _load_from_ini_file(config_file, first_section)

    return None


def _load_from_ini_file(path, section_name) -> Config:
    parser = ConfigParser()
    parser.read(path)

    if section_name not in parser.sections():
        raise ValueError(f"[{section_name}] not found in configuration file.")

    section = parser[section_name]

    if "url" not in section:
        raise ValueError(f"[url] not found in configuration.")

    return Config(section["url"], section.get("api_token"))


def _try_load_from_environment_vars():
    url = os.getenv("FEYN_QLATTICE_URL", None)
    api_token = os.getenv("FEYN_QLATTICE_API_TOKEN", None)

    if url:
        return Config(url, api_token)

    # Backwards compatability
    url = os.getenv("QLATTICE_BASE_URI", None)
    api_token = os.getenv("FEYN_TOKEN", None)

    if url is not None:
        warnings.warn("Please use the [FEYN_QLATTICE_URL]. [QLATTICE_BASE_URI] has been deprecated and will stop working in next version of feyn.", DeprecationWarning)

    if api_token is not None:
        warnings.warn("Please use the [FEYN_QLATTICE_API_TOKEN]. [FEYN_TOKEN] has been deprecated and will stop working in next version of feyn.", DeprecationWarning)

    if url:
        return Config(url, api_token)
    else:
        return None


def _find_config_file():
    existing_config_files = [x for x in _config_file_paths if x.exists()]

    if len(existing_config_files) > 1:
        raise ValueError(f"Multiple configuration files found: {[str(x) for x in existing_config_files]}.")

    if existing_config_files:
        return existing_config_files[0]

    return None


def _get_first_section(path):
    parser = ConfigParser()
    parser.read(path)
    section_names = parser.sections()

    if not section_names:
        raise ValueError(f"No sections found in configuration file.")

    return section_names[0]
