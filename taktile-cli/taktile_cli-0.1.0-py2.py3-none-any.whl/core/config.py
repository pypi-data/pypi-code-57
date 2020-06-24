import os
from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    USERS_OPEN_REGISTRATION: bool = False
    IN_TESTING = False

    DEBUG: bool = False
    WEB_UR: str = "www.taktile.com"
    TAKTILE_API_HOST: str = "http://taktile-api.local.tktl.io"
    DEPLOYMENT_API_HOST: str = "http://deployment-api.local.tktl.io"
    LOG_HOST: str = "http://logs.local.tktl.io"

    TKTL_CONFIG_PATH: str = os.path.expanduser("~/.tktl")
    CONFIG_FILE_NAME: str = "config.json"
    TAKTILE_API_KEY: str = None
    HELP_HEADERS_COLOR: str = "yellow"
    HELP_OPTIONS_COLOR: str = "green"
    USE_CONSOLE_COLORS: str = True
    HELP_COLORS_DICT: Dict = {
        "help_headers_color": "yellow",
        "help_options_color": "green",
    }

    class Config:
        case_sensitive = True


settings = Settings()
