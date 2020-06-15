#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import os
import pathlib
import textwrap
from typing import Dict, Optional

from termcolor import colored

from .. import util

CONFIG_API_KEY_LABEL = "api_key"
CONFIG_API_KEY_ENV_VAR = "MODELZOO_API_KEY"

CONFIG_BASE_API_URL_LABEL = "base_api_url"
CONFIG_BASE_API_URL_ENV_VAR = "MODELZOO_BASE_API_URL"
DEFAULT_BASE_API_URL = "https://api.modelzoo.dev/v1/"

LOGIN_URL = "{}/profile".format(util.BASE_UI_URL)


def get_config_file() -> pathlib.Path:
    return pathlib.Path.home().joinpath(".modelzoo").joinpath("config.json")


def get_config() -> Dict:
    # TODO: Support multiple file types (yaml, toml)
    config_file = pathlib.Path(str(get_config_file()))
    if config_file.exists():
        with config_file.open("r") as fp:
            return json.load(fp)
    else:
        return {}


def get_base_api_url() -> str:
    base_api = os.getenv(CONFIG_BASE_API_URL_ENV_VAR, None)
    if base_api:
        return base_api

    base_api = get_config().get(CONFIG_BASE_API_URL_LABEL)
    if base_api:
        return base_api

    return DEFAULT_BASE_API_URL


def get_api_key(api_key: Optional[str] = None) -> str:
    """
    Get the API key associated with the existing environment.

    Uses the following ordering for priority:

        1. api_key argument passed to this function
        2. environment variables
        3. configuration file in home directory.

    If no key is found, then the user is prompted for a key.
    """
    if api_key:
        return api_key

    _api_key = os.getenv(CONFIG_API_KEY_ENV_VAR, None)
    if _api_key:
        return _api_key

    config = get_config()
    if config.get(CONFIG_API_KEY_LABEL):
        return config[CONFIG_API_KEY_LABEL]

    return save_api_key()


def save_api_key(api_key: Optional[str] = None, silent: bool = False) -> str:
    if not api_key and not silent:
        api_key = _prompt_api_key()

    # Use the existing configuration if it already exists.
    config = get_config()
    config[CONFIG_API_KEY_LABEL] = api_key

    config_file = get_config_file()
    config_file.parent.mkdir(parents=False, exist_ok=True)
    with config_file.open("w") as fp:
        json.dump(config, fp)

    print("Saved configuration file at {}".format(str(config_file)))

    return api_key


def _prompt_api_key() -> str:
    print(r"                                                ")
    print(r"  __  __           _      _   _____             ")
    print(r" |  \/  | ___   __| | ___| | |__  /___   ___    ")
    print(r" | |\/| |/ _ \ / _` |/ _ \ |   / // _ \ / _ \   ")
    print(r" | |  | | (_) | (_| |  __/ |  / /| (_) | (_) |  ")
    print(r" |_|  |_|\___/ \__,_|\___|_| /____\___/ \___/   ")
    print(r"                                                ")
    print(
        "\n".join(
            textwrap.wrap(
                "Open the URL below to create or access your account. Once "
                "you've created an account, copy-paste the api key below to "
                "configure this environment."
            )
        )
    )
    print("")
    print(colored(LOGIN_URL, "green"))
    print("")
    return input("API Key: ")


def auth(api_key: Optional[str] = None) -> str:
    """
    Initialize or overwrite the API key used by this environment. This will
    edit or create the configuration file (`~/.modelzoo/config.json`).

    Arguments:
        api_key: Optional string API key. If not provided, this function will
        prompt the user to input an API key.

    Returns:
        The API key
    """
    return save_api_key(api_key=api_key, silent=False)
