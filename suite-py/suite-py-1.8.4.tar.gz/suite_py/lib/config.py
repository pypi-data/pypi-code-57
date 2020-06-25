# -*- encoding: utf-8 -*-
import os
import json
import sys
import yaml

from suite_py.lib.singleton import Singleton
from suite_py.lib.logger import Logger

logger = Logger()


class Config(metaclass=Singleton):
    _config = {}
    _config_path_file = os.path.join(os.environ["HOME"], ".suite_py/config.yml")
    _base_cache_path = os.path.join(os.environ["HOME"], ".suite_py/cache")

    def __init__(self):
        if not os.path.exists(self._base_cache_path):
            os.makedirs(self._base_cache_path)

    def load(self):
        with open(self._config_path_file) as configfile:
            self._config = yaml.safe_load(configfile)

        self._config["user"]["projects_home"] = os.path.join(
            os.environ["HOME"], self._config["user"]["projects_home"]
        )

        self._config["user"].setdefault("review_channel", "#review")

        self._config["user"].setdefault("deploy_channel", "#deploy")

        self._config["user"].setdefault("default_slug", "PRIMA-XXX")

        self._config["user"].setdefault("captainhook_timeout", 30)  # This is in seconds

        self._config["user"].setdefault(
            "captainhook_url", "http://captainhook-internal.prima.it"
        )

        self.load_local_config()

        return self._config

    def load_local_config(self):
        local_conf_path = os.path.join(os.curdir, ".suite_py.yml")
        try:
            with open(local_conf_path) as f:
                local_conf = yaml.safe_load(f)

        except FileNotFoundError:
            return

        for key, value in local_conf["user"].items():
            self._config["user"][key] = value

    def put_cache(self, key, data):
        with open(os.path.join(self._base_cache_path, key), "w") as cache_file:
            json.dump(data, cache_file)

    def get_cache(self, key):
        try:
            with open(os.path.join(self._base_cache_path, key)) as cache_file:
                return json.load(cache_file)
        except Exception:
            logger.error(
                f"Non ho trovato nessuna versione in cache per la chiave {key}. Attiva la VPN."
            )
            sys.exit(-1)
