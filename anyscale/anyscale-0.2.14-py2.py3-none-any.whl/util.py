import datetime
import json
import logging
import os
import re
import sys
import threading
import time
from typing import Any, Dict, Iterator, List
import unicodedata

import boto3
import botocore
from botocore.config import Config
import click
import requests
import yaml

from anyscale.common import ENDPOINTS
import anyscale.conf


logger = logging.getLogger(__file__)

BOTO_MAX_RETRIES = 5


def confirm(msg: str, yes: bool) -> Any:
    return None if yes else click.confirm(msg, abort=True)


def get_endpoint(endpoint: str) -> str:
    if endpoint.startswith("/"):
        route = endpoint
    else:
        route = ENDPOINTS[endpoint]
    return "{}{}".format(anyscale.conf.ANYSCALE_HOST, route)


def load_credentials() -> str:
    # The environment variable ANYSCALE_CLI_TOKEN can be used to
    # overwrite the credentials in ~/.anyscale/credentials.json
    if "ANYSCALE_CLI_TOKEN" in os.environ:
        return os.environ["ANYSCALE_CLI_TOKEN"]
    path = os.path.expanduser("~/.anyscale/credentials.json")
    if not os.path.exists(path):
        raise click.ClickException(
            "Credentials not found. You need to create an account at {0} "
            "and then go to {0}/credentials and follow the instructions.".format(
                anyscale.conf.ANYSCALE_HOST
            )
        )
    with open(path) as f:
        try:
            credentials: Dict[str, str] = json.load(f)
        except json.JSONDecodeError:
            msg = (
                "Unable to load user credentials.\n\nTip: Try creating your "
                "user credentials again by going to {}/credentials and "
                "following the instructions. If this does not work, "
                "please contact Anyscale support!".format(anyscale.conf.ANYSCALE_HOST)
            )
            raise click.ClickException(msg)
    if "cli_token" not in credentials:
        raise click.ClickException("Credential file not valid, please regenerate it.")
    return credentials["cli_token"]


def send_json_request(
    endpoint: str, json_args: Dict[str, Any], method: str = "GET"
) -> Dict[str, Any]:
    if anyscale.conf.CLI_TOKEN is None:
        anyscale.conf.CLI_TOKEN = load_credentials()

    url = get_endpoint(endpoint)
    cookies = {"cli_token": anyscale.conf.CLI_TOKEN}
    try:
        if method == "GET":
            resp = requests.get(url, params=json_args, cookies=cookies)
        elif method == "POST":
            resp = requests.post(url, json=json_args, cookies=cookies)
        elif method == "DELETE":
            resp = requests.delete(url, json=json_args, cookies=cookies)
        elif method == "PATCH":
            resp = requests.patch(url, data=json_args, cookies=cookies)
        else:
            assert "unknown method {}".format(method)
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Failed to connect to anyscale server at {}".format(url)
        )

    if not resp.ok:
        raise click.ClickException("{}: {}.".format(resp.status_code, resp.text))

    if resp.status_code == 204:
        return {}

    json_resp: Dict[str, Any] = resp.json()
    if "error" in json_resp:
        raise click.ClickException("{}".format(json_resp["error"]))

    return json_resp


def serialize_datetime(d: datetime.datetime) -> str:
    # Make sure that overwriting the tzinfo in the line below is fine.
    # Note that we have to properly convert the timezone if one is
    # already specified. This can be done with the .astimezone method.
    assert d.tzinfo is None
    return d.replace(tzinfo=datetime.timezone.utc).isoformat()


def deserialize_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f+00:00")


def humanize_timestamp(timestamp: datetime.datetime) -> str:
    delta = datetime.datetime.utcnow() - timestamp
    offset = float(delta.seconds + (delta.days * 60 * 60 * 24))
    delta_s = int(offset % 60)
    offset /= 60
    delta_m = int(offset % 60)
    offset /= 60
    delta_h = int(offset % 24)
    offset /= 24
    delta_d = int(offset)

    if delta_d >= 1:
        return "{} day{} ago".format(delta_d, "s" if delta_d > 1 else "")
    if delta_h > 0:
        return "{} hour{} ago".format(delta_h, "s" if delta_h > 1 else "")
    if delta_m > 0:
        return "{} minute{} ago".format(delta_m, "s" if delta_m > 1 else "")
    else:
        return "{} second{} ago".format(delta_s, "s" if delta_s > 1 else "")


def execution_log_name(session_command_id: int) -> str:
    return "/tmp/ray_command_output_{session_command_id}".format(
        session_command_id=session_command_id
    )


def startup_log_name(session_id: int) -> str:
    return "/tmp/session_startup_logs_{session_id}".format(session_id=session_id)


def slugify(value: str) -> str:
    """
    Code adopted from here https://github.com/django/django/blob/master/django/utils/text.py

    Convert  to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Also strip leading and trailing whitespace.
    """

    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[-\s]+", "-", value)


def get_cluster_config(config_path: str) -> Any:
    with open(config_path) as f:
        cluster_config = yaml.safe_load(f)

    return cluster_config


def get_requirements(requirements_path: str) -> str:
    with open(requirements_path) as f:
        return f.read()


def _resource(name: str, region: str) -> Any:
    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    boto_session = boto3.session.Session()
    return boto_session.resource(name, region, config=boto_config)


def _client(name: str, region: str) -> Any:
    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    boto_session = boto3.session.Session()
    return boto_session.client(name, region, config=boto_config)


def _get_role(role_name: str, region: str) -> Any:
    iam = _resource("iam", region)
    role = iam.Role(role_name)
    try:
        role.load()
        return role
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def _get_user(user_name: str, region: str) -> Any:
    iam = _resource("iam", region)
    user = iam.User(user_name)
    try:
        user.load()
        return user
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def get_available_regions() -> List[str]:
    boto_session = boto3.session.Session()
    client = boto_session.client("ec2")
    return [region["RegionName"] for region in client.describe_regions()["Regions"]]


class Timer:
    """
    Code adopted from https://stackoverflow.com/a/39504463/3727678

    Spawn thread and time process that may be blocking.
    """

    def timer_generator(self) -> Iterator[str]:
        while True:
            time_diff = time.gmtime(time.time() - self.start_time)
            yield "{0}: {1}".format(self.message, time.strftime("%M:%S", time_diff))

    def __init__(self, message: str = "") -> None:
        self.message = message
        self.busy = False
        self.start_time = 0.0

    def timer_task(self) -> None:
        while self.busy:
            sys.stdout.write(next(self.timer_generator()))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b" * (len(self.message) + 20))
            sys.stdout.flush()

    def start(self) -> None:
        self.busy = True
        self.start_time = time.time()
        threading.Thread(target=self.timer_task).start()

    def stop(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()
        self.busy = False
        self.start_time = 0.0
        time.sleep(1)
