import json
from functools import wraps

import requests

from tktl.core.config import settings
from tktl.core.exceptions import InvalidInputError, AuthenticationError
from tktl.core.loggers import CliLogger
from tktl.core.managers.auth import AuthConfigManager
from tktl.core.strings import CLIStrings, HeaderStrings

UNAUTHORIZED_EXTENDED_INFO = (
    "\n\nNote: Please keep in mind that currently you can login only with the email and "
    "password from your Paperspace account. If you're using AD, SAML or GitHub "
    "credentials, please log into the Paperspace Console and create an API key for use with "
    "the CLI client. For more information, please refer to the CLI client documentation."
)

logger = CliLogger()


def is_error_or_missing_keys_print(res, *required_keys):
    if "error" in res:
        if "message" in res:
            print(res["message"])
            return True
        if "message" in res["error"]:
            error_message = res["error"]["message"] + UNAUTHORIZED_EXTENDED_INFO
            print(error_message)
            return True
        print(json.dumps(res, indent=2, sort_keys=True))
        return True
    elif not all(key in res for key in required_keys):
        if "message" in res:
            print(res["message"])
            return True
        print(json.dumps(res, indent=2, sort_keys=True))
        return True
    return False


def login(user_name=None, password=None, api_key=None):
    """

    Parameters
    ----------
    user_name
    password
    api_key

    Returns
    -------

    """

    if not api_key and not (user_name and password):
        raise InvalidInputError(
            CLIStrings.INVALID_INPUT + "either username and password or "
            "api_key must be provided"
        )

    if api_key:
        AuthConfigManager.set_api_key(api_key)
        return True
    else:
        params = {"username": user_name, "password": password}
        r = requests.post(
            f"{settings.TAKTILE_API_HOST}{settings.API_V1_STR}/keys/create",
            headers={
                "Accept": HeaderStrings.APPLICATION_JSON,
                "Content-Type": HeaderStrings.APPLICATION_URLENCODED,
            },
            data=params,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {r.json()["detail"]}')
            return False
        res = r.json()
        api_key = res["api_key"]
        AuthConfigManager.set_api_key(api_key)
    return True


def set_api_key(api_key):
    AuthConfigManager.set_api_key(api_key=api_key)
    path = (
        f"{AuthConfigManager.get_tktl_config_path()}/"
        f"{AuthConfigManager.SETTINGS.CONFIG_FILE_NAME}"
    )
    logger.log(f"Successfully added your API Key to {path} You're ready to go!")
    return True


def logout():
    AuthConfigManager.clear_tktl_config()
    return True


def validate_key(suppress=False):
    key = AuthConfigManager.get_api_key()
    if not key:
        logger.error(CLIStrings.AUTH_ERROR_MISSING_KEY)
        raise AuthenticationError(CLIStrings.AUTH_ERROR_MISSING_KEY)

    r = requests.get(
        f"{settings.TAKTILE_API_HOST}{settings.API_V1_STR}/users/me",
        headers={"Accept": HeaderStrings.APPLICATION_JSON, "X-Api-Key": key},
    )
    try:
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f'Request failed: {r.json()["detail"]}')
        return False

    if not suppress:
        logger.log("Login successful!", color="green")
    return True


def validate_decorator(func):
    @wraps(func)
    def wrapped_validation(*args, **kwargs):
        validate_key(suppress=True)
        return func(*args, **kwargs)

    return wrapped_validation
