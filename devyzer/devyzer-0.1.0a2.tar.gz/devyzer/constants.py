# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

EXIT = "EXIT"
DEFAULT_LOG_LEVEL = "INFO"
ENV_LOG_LEVEL = "LOG_LEVEL"
DEFAULT_LOG_LEVEL_LIBRARIES = "ERROR"
ENV_LOG_LEVEL_LIBRARIES = "LOG_LEVEL_LIBRARIES"

# Endpoints
BOT_SOCKET_IO_ENDPOINT = os.getenv('BOT_SOCKET_IO_ENDPOINT', "https://bot.devyzer.io")
CONSOLE_ENDPOINT = os.getenv('CONSOLE_ENDPOINT', "https://staging.devyzer.io")
GATEWAY_ENDPOINT = os.getenv('GATEWAY_ENDPOINT', "https://gateway.devyzer.io")
AUTOCOMPLETE_ENDPOINT = os.getenv('GATEWAY_ENDPOINT', "https://cli-suggester.devyzer.io")

AUTH_UI_ENDPOINT = lambda token: f'{CONSOLE_ENDPOINT}/cli/grant/{token}'
AUTH_ENDPOINT = lambda token: f'{GATEWAY_ENDPOINT}/cli/{token}'
AUTH_GITHUB_ENDPOINT = lambda token: f'{GATEWAY_ENDPOINT}/check/github/{token}'
AUTH_CREATE_ENDPOINT = f'{GATEWAY_ENDPOINT}/cli/create'
LINK_GITHUB_UI_ENDPOINT = f'{CONSOLE_ENDPOINT}/cli/link-github'

# others
CONNECTING_TIMEOUT = 50
AUTHORIZED_EXPIRY = 3  # in minutes
CONSOLE_TOKEN = None

DEFAULT_CONFIG_NAME = ".devyzer.json"
