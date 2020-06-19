import logging
import sys
from os import path
from pathlib import Path
from pprint import pformat
from urllib.parse import urljoin, urlparse

import click
import fsspec
import requests
import yaml

from nomnomdata.auth import DEFAULT_PROFILE, NNDAuth, get_profiles

from .model_validator import validate_model

_logger = logging.getLogger(__name__)


class NomitallSession(requests.Session):
    def __init__(self, prefix_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        _logger.info(f"Request {method}:{url}")
        return super().request(method, url, *args, **kwargs)


def fetch_yaml(relpath):
    return yaml.full_load(Path(relpath).read_text())


def fetch_include(fpath, model_fp):
    final_path = (Path(path.abspath(model_fp)).parent / Path(fpath)).resolve()
    return yaml.full_load(final_path.read_text())


def include_includes(parameters, model_fp):
    parsed_params = []
    assert isinstance(
        parameters, list
    ), "Parameters lists must be a list of dictionaries ( `- foo:bar` , not `foo:bar` )"
    for parameter in parameters:
        assert isinstance(
            parameter, dict
        ), "Parameters lists must be a list of dictionaries ( `- foo:bar` , not `foo:bar` )"
        if "parameters" in parameter:
            parameter["parameters"] = include_includes(parameter["parameters"], model_fp)
            parsed_params.append(parameter)
        elif "include" in parameter:
            for include in parameter["include"]:
                _logger.info("\tIncluding file {include}")
                include_doc = fetch_include(include, model_fp)
                _logger.debug(f"FETCHED INCLUDE: \n{pformat(include_doc)}")
                _logger.debug("PARSING FETCHED FOR INCLUDES")
                include_doc = include_includes(include_doc, model_fp)
                _logger.debug(
                    f"FETCHED INCLUDE AFTER RESCURSIVE INCLUDE: \n{pformat(include_doc)}"
                )
                parsed_params.extend(include_doc)
        else:
            parsed_params.append(parameter)
    return parsed_params


@click.command()
@click.option(
    "-n",
    "--nomitall",
    default="nomitall-stage",
    help="Specify the nomitall to update [nomitall-prod,nomitall-stage,custom_url]",
)
@click.option(
    "-dr",
    "--dry_run",
    "--dry-run",
    is_flag=True,
    help="Do not update nomitall, just output parsed model json",
)
@click.option(
    "-f",
    "--file",
    "model_fn",
    default="model.yaml",
    help="Model YAML file to build + deploy",
)
@click.option(
    "-o", "--org", "org", help="UUID of the organization to publish the model as",
)
def model_update(
    work_dir=None,
    nomitall_secret=None,
    nomitall=None,
    dry_run=None,
    model_fn=None,
    org=None,
):
    """Update staging or prod nomitall model definitions. Defaults to using files from git master/staging branch for prod/staging"""
    if nomitall == "nomitall-prod":
        nomitall_url = "https://user.api.nomnomdata.com/api/1/"
    elif nomitall == "nomitall-stage":
        nomitall_url = "https://staging.user.api.nomnomdata.com/api/1/"
    else:
        nomitall_url = nomitall
    if not org:
        profile = get_profiles()[DEFAULT_PROFILE]
        netloc = urlparse(nomitall_url).netloc
        org = profile[netloc]["default-org"]
    doc = yaml.full_load(Path(model_fn).read_text())
    model_type = doc.get("type")
    if not model_type:
        _logger.error("Model does not have a type, this is required")
        sys.exit(1)
    # add legacy model verison if it doesn't exit
    if model_type == "engine":
        for action, action_dict in doc["actions"].items():
            _logger.info("Parsing {}".format(action))
            action_dict["parameters"] = include_includes(
                action_dict["parameters"], model_fn
            )
    else:
        doc["parameters"] = include_includes(doc["parameters"], model_fn)

    if not validate_model(doc):
        raise click.Abort("Model did not pass validation")

    if dry_run:
        _logger.info("PARSED MODEL :")
        _logger.info(pformat(doc))
        sys.exit()

    update_model(nomitall_url, nomitall_secret, doc, model_type, org)


def upload_icons(icons, uuid, session):
    _logger.info("Pushing icons to nomitall")
    icon_files = {}
    for size, icon_uri in icons.items():
        openfile = fsspec.open(icon_uri, mode="rb")
        with openfile as f:
            icon_files[size] = f.read()
    resp = session.request("POST", f"engine/upload-icons/{uuid}", files=icon_files)
    check_response(resp)


def upload_help(help_files, uuid, session):
    _logger.info("Pushing mds to nomitall")
    resp = session.request("POST", f"engine/upload-md/{uuid}", files=help_files)
    check_response(resp)


def load_help_file(md_path):
    _logger.info(f"Loading {md_path}")
    openfile = fsspec.open(md_path, mode="rb")
    with openfile as f:
        md_file = f.read()
    return md_file


def process_help(doc, key="root"):
    help_files = {}
    if isinstance(doc, list):
        for subele in doc:
            help_files.update(process_help(subele, key=key))
    if isinstance(doc, dict):
        process_help
        for k, subele in doc.items():
            if k == "help":
                if "file" in subele:
                    if "name" in doc:
                        key += "." + doc["name"]
                    help_files[key] = load_help_file(subele["file"])
                    doc[k] = {"key": key}
            else:
                help_files.update(process_help(subele, key=".".join([key, k]),))
    return help_files


def update_model(nomitall_url, nomitall_secret, model, model_type, org):
    session = NomitallSession(prefix_url=nomitall_url)
    session.auth = NNDAuth()
    help_files = {}
    icons = {}
    if model_type == "engine":
        help_files = process_help(model)
        icons = model.pop("icons", {})
        uuid = model["uuid"]
        _logger.info("Pushing engine to nomitall")
        resp = session.request("POST", f"engine/deploy/{org}", json=model)
        check_response(resp)
        upload_help(help_files=help_files, uuid=uuid, session=session)
        upload_icons(icons=icons, uuid=uuid, session=session)

    elif model_type == "shared_object_type":
        _logger.info("Pushing shared object type to nomitall")
        resp = session.request("POST", "shared_object_type/update", json=model)
        check_response(resp)

    elif model_type == "connection":
        _logger.info("Pushing connection type to nomitall")
        resp = session.request("POST", "connection_type/update", json=model)
        check_response(resp)


def check_response(resp):
    if not resp.ok:
        if resp.status_code == 500:
            _logger.error(f"Internal server error\n{resp.text}")
            raise click.Abort
        reply_data = resp.json()
        if reply_data.get("error"):
            raise click.Abort(str(reply_data))
        if reply_data.get("status"):
            if reply_data["status"] == "success":
                _logger.info("Request successful")
        if resp.status_code == 401:
            _logger.error(f"Check secret key is valid\n\t\t {resp.json()}")
            raise click.Abort
        if resp.status_code == 403:
            _logger.error(f"Check user permissions\n\t\t {resp.json()}")
            raise click.Abort
    resp.raise_for_status()
