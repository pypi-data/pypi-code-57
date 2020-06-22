import os
import time
import yaml
import google.auth.crypt
import google.auth.jwt
from itertools import product
from typing import Dict, Tuple, Union
from google.oauth2.service_account import Credentials
from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
from google.auth.transport.requests import Request
from google.auth.iam import Signer

MAX_TOKEN_LIFETIME_SECS = 12 * 3600  # seconds
CONFIG_TYPE = Dict[str, Union[str, Dict[str, str]]]


def load_client_configuration(configuration_path: str) -> CONFIG_TYPE:
    """
    This reads the configuration file in yaml format and returns the configuration as a dictionary.
    It also validates the format of the configuration to ensure all the necessary fields are present.
    :param configuration_path: The location of the configuration file.
    :type configuration_path: str
    :return: The parsed configuration.
    :rtype: Dict[str, Union[str, Dict[str, str]]]
    :raises: KeyError, TypeError, FileNotFoundError
    """
    if os.path.exists(configuration_path):
        if configuration_path.endswith(".yaml") or configuration_path.endswith(".yml") or \
                configuration_path.endswith(".json"):
            with open(configuration_path, "r") as stream:
                configuration = yaml.safe_load(stream)
            svc_config = configuration.get("service")
            if svc_config is not None and \
                    all(j in svc_config and k in svc_config[j]
                        for j, k in product(["production", "development"],
                                            ["host", "api_key", "service_account_credentials", "authentication"])):
                return configuration
            raise KeyError("load_client_configuration: Configuration file is missing keys.")
        raise TypeError(f"load_client_configuration: The configuration file must be a yaml file or a json file "
                        f"with extensions '.yaml', '.yml', or '.json'.  The configuration path given was "
                        f"{configuration_path}")
    raise FileNotFoundError(f"load_configuration: The file {configuration_path} does not exist!")


def generate_jwt_token_from_impersonated_account(service_account_info: Dict[str, str], audiences: str,
                                                 issuer: str) -> Tuple[str, int]:
    """
    Using a dictionary containing the information from a Google Cloud service account credentials file, this function
    impersonates the Company Information API master user service account and signs a JSON Web Token (JWT) used to
    authenticate the client when accessing the service.
    :param service_account_info: A dictionary containing all the information found in a Google Cloud service account
    credentials JSON file.
    :type service_account_info: Dict[str, str]
    :param audiences: The intended recipient of the JWT. Found in the Google Endpoint specification. For example,
    for the company information API, the recipient is 'company-information.api.willowlabs.ai'
    :type audiences: str
    :param issuer: The email address of the impersonated API master user service account.
    :type issuer: str
    :param jwt_lifetime: The length of time, in seconds, for which the created JWT is valid.
    :type jwt_lifetime: int
    :return: A tuple containing the JWT and a POSIX/Unix epoch-style timestamp indicating when the JWT expires.
    :rtype: Tuple[str, int]
    """
    credentials = Credentials.from_service_account_info(service_account_info,
                                                        scopes=["https://www.googleapis.com/auth/cloud-platform",
                                                                "https://www.googleapis.com/auth/iam"])
    if not credentials.valid:
        credentials.refresh(Request())
    impersonated_credentials = ImpersonatedCredentials(source_credentials=credentials, target_principal=issuer,
                                                       target_scopes=["https://www.googleapis.com/auth/cloud-platform",
                                                                      "https://www.googleapis.com/auth/iam"])
    if not impersonated_credentials.valid:
        impersonated_credentials.refresh(Request())

    signer = Signer(Request(), impersonated_credentials, impersonated_credentials.service_account_email)
    now = int(time.time())
    expires = now + MAX_TOKEN_LIFETIME_SECS

    payload = {
        'iat': now,
        'exp': expires,
        'aud': audiences,
        'iss': issuer
    }
    return google.auth.jwt.encode(signer, payload).decode("utf-8"), expires
