# -*- coding: utf-8 -*-

import os
import tuxbuild.exceptions
from os.path import expanduser
import configparser
import re
import requests
import yaml
import time


class Config:
    def __init__(self, config_path="~/.config/tuxbuild/config.ini"):
        """
            Retrieve tuxbuild authentication token and API url

            Tuxbuild requires an API token. Optionally, a API url endpoint may
            be specified. The API url defaults to https://api.tuxbuild.com/v1.

            The token and url may be specified in environment variables, or in
            a tuxbuild config file. If using the config file, the environment
            variable TUXBUILD_ENV may be used to specify which tuxbuild config
            to use.

            Environment variables:
                TUXBUILD_TOKEN
                TUXBUILD_URL (optional)

            Config file:
                Must be located at ~/.config/tuxbuild/config.ini.
                This location can be overriden by setting the TUXBUILD_CONFIG
                environment variable.
                A minimum config file looks like:

                    [default]
                    token=vXXXXXXXYYYYYYYYYZZZZZZZZZZZZZZZZZZZg

                Multiple environments may be specified. The environment named
                in TUXBUILD_ENV will be chosen. If TUXBUILD_ENV is not set,
                'default' will be used.

                Fields:
                    token
                    api_url (optional)
        """

        self.default_api_url = (
            "https://api.tuxbuild.com/v1"  # Use production v1 if no url is specified
        )
        self.tuxbuild_env = os.getenv("TUXBUILD_ENV", "default")

        (self.auth_token, self.kbapi_url) = self._get_config_from_env()

        if os.getenv("TUXBUILD_CONFIG"):
            config_path = os.getenv("TUXBUILD_CONFIG")

        if not self.auth_token:
            (self.auth_token, self.kbapi_url) = self._get_config_from_config(
                config_path
            )

        if not self.auth_token:
            raise tuxbuild.exceptions.TokenNotFound(
                "Token not found in TUXBUILD_TOKEN nor at [{}] in {}".format(
                    self.tuxbuild_env, config_path
                )
            )
        if not self.kbapi_url:
            raise tuxbuild.exceptions.URLNotFound(
                "TUXBUILD_URL not set in env, or api_url not specified at [{}] in {}.".format(
                    self.tuxbuild_env, config_path
                )
            )

    def _get_config_from_config(self, config_path):
        path = expanduser(config_path)
        try:
            open(path, "r")  # ensure file exists and is readable
        except Exception as e:
            raise tuxbuild.exceptions.CantGetConfiguration(str(e))

        config = configparser.ConfigParser()

        config.read(path)
        if not config.has_section(self.tuxbuild_env):
            raise tuxbuild.exceptions.InvalidConfiguration(
                "Error, missing section [{}] from config file '{}'".format(
                    self.tuxbuild_env, path
                )
            )
        kbapi_url = (
            config[self.tuxbuild_env].get("api_url", self.default_api_url).rstrip("/")
        )
        auth_token = config[self.tuxbuild_env].get("token", None)
        return (auth_token, kbapi_url)

    def _get_config_from_env(self):
        # Check environment for TUXBUILD_TOKEN
        auth_token = None
        kbapi_url = None
        if os.getenv("TUXBUILD_TOKEN"):
            auth_token = os.getenv("TUXBUILD_TOKEN")
            kbapi_url = os.getenv("TUXBUILD_URL", self.default_api_url).rstrip("/")
        return (auth_token, kbapi_url)

    def get_auth_token(self):
        return self.auth_token

    def get_kbapi_url(self):
        return self.kbapi_url

    def get_tuxbuild_env(self):
        return self.tuxbuild_env

    def check_auth_token(self):
        headers = {"Content-type": "application/json", "Authorization": self.auth_token}
        url = self.kbapi_url + "/verify"
        attempts = 6
        for i in range(1, attempts + 1):
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return
            elif r.status_code // 500 == 1:
                if i < attempts:
                    time.sleep(2 ** i)  # exponential backoff
            else:
                r.raise_for_status()  # Some unexpected status that's not caught


InvalidConfiguration = tuxbuild.exceptions.InvalidConfiguration


class BuildSetConfig:
    def __init__(self, set_name, filename=None):
        self.set_name = set_name
        if filename:
            self.filename = filename
        else:
            self.filename = os.path.expanduser("~/.config/tuxbuild/builds.yaml")
        self.entries = []
        self.__load_config__()

    def __load_config__(self):
        filename = self.filename
        set_name = self.set_name
        try:
            if re.match(r"^https?://", str(filename)):
                contents = self.__fetch_remote_config__(filename)
            else:
                contents = open(filename).read()
            config = yaml.safe_load(contents)
        except (FileNotFoundError, yaml.loader.ParserError) as e:
            raise InvalidConfiguration(str(e))
        if not config:
            raise InvalidConfiguration(
                f"Build set configuration in {filename} is empty"
            )
        if "sets" not in config:
            raise InvalidConfiguration('Missing "sets" key')
        for set_config in config["sets"]:
            if set_config["name"] == set_name:
                if "builds" in set_config:
                    self.entries = set_config["builds"]
                    if not self.entries:
                        raise InvalidConfiguration(
                            f'Build list is empty for set "{set_name}"'
                        )
                    return
                else:
                    raise InvalidConfiguration(
                        f'No "builds" field defined for set "{set_name}"'
                    )
        raise InvalidConfiguration(f'No build set named "{set_name}" in {filename}')

    def __fetch_remote_config__(self, url, retries=3, sleep=3):
        result = requests.get(url)
        if result.status_code != 200:
            if retries == 0 or result.status_code // 500 != 1:
                raise InvalidConfiguration(f"Unable to retrieve {url}: {result.reason}")
            time.sleep(sleep)
            return self.__fetch_remote_config__(url, retries - 1, sleep * 2)
        return result.text
