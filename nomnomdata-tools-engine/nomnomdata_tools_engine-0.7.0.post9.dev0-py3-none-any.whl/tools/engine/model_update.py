import functools
import logging
import sys
from os import getcwd, path
from pathlib import Path
from pprint import pformat
from subprocess import check_output
from urllib.parse import urljoin, urlparse

import click
import fsspec
import requests
import yaml
from git import Repo

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


def confirmation_prompt(question):
    reply = input(question + " (y or n): ")
    if reply[0] == "y":
        return True
    if reply[0] == "n":
        return False
    else:
        return confirmation_prompt("Please enter ")


@functools.lru_cache()
def fetch_remote_git_yaml(remote_url, git_ref, file_path):
    cmd = "git archive --remote={} {} {} | tar -xO".format(remote_url, git_ref, file_path)
    file_str = check_output(cmd, shell=True).decode()
    return yaml.full_load(file_str)


def fetch_git_yaml(relpath, git_ref):
    if git_ref:
        repo = Repo(".", search_parent_directories=True)
        reldir = path.relpath(getcwd(), repo.working_dir)
        git_path = path.join(reldir, relpath)
        _logger.info("\tUsing {} at ref {}, will fetch latest".format(git_path, git_ref))
        for fetch_info in repo.remotes["origin"].fetch():
            _logger.info("\tUpdated %s to %s" % (fetch_info.ref, fetch_info.commit))
        model_str = repo.git.show("{}:{}".format(git_ref, git_path))
        return yaml.full_load(model_str)
    else:
        with open(relpath, "r") as f:
            _logger.info("Using {} from current working directory".format(relpath))
            return yaml.full_load(f)


def confirm_git_branch(work_dir, nomitall):
    if work_dir:
        if nomitall == "nomitall-prod":
            question = "You are about to push your working directory to production!\
            Are you absolutely sure you want to do this?"

            if not confirmation_prompt(question):
                _logger.info("You have chosen wisely")
                sys.exit()
            if not confirmation_prompt("Absolutely sure?"):
                _logger.info("You have chosen wisely")
                sys.exit()
        branch = None
    else:
        if nomitall == "nomitall-prod":
            branch = "origin/master"
        elif nomitall == "nomitall-stage":
            branch = "origin/staging"
    return branch


def fetch_include(fpath, git_ref, model_fp, remote=None):
    if remote:
        return fetch_remote_git_yaml(remote, git_ref, fpath)
    else:
        final_path = Path(path.abspath(model_fp)).parent / Path(fpath)
        return fetch_git_yaml(final_path.resolve(), git_ref)


def include_includes(parameters, git_ref, model_fp, remote=None):
    parsed_params = []
    assert isinstance(
        parameters, list
    ), "Parameters lists must be a list of dictionaries ( `- foo:bar` , not `foo:bar` )"
    for parameter in parameters:
        assert isinstance(
            parameter, dict
        ), "Parameters lists must be a list of dictionaries ( `- foo:bar` , not `foo:bar` )"
        if "parameters" in parameter:
            parameter["parameters"] = include_includes(
                parameter["parameters"], git_ref, model_fp
            )
            parsed_params.append(parameter)
        elif "include" in parameter:
            for include in parameter["include"]:
                _logger.info(
                    "\tIncluding file {} from {}@{}".format(include, remote, git_ref)
                )
                include_doc = fetch_include(include, git_ref, model_fp, remote)
                _logger.debug(f"FETCHED INCLUDE: \n{pformat(include_doc)}")
                _logger.debug("PARSING FETCHED FOR INCLUDES")
                include_doc = include_includes(include_doc, git_ref, model_fp, remote)
                _logger.debug(
                    f"FETCHED INCLUDE AFTER RESCURSIVE INCLUDE: \n{pformat(include_doc)}"
                )
                parsed_params.extend(include_doc)
        elif "include_git" in parameter:
            for include in parameter["include_git"]:
                new_remote, new_ref, fpath = include.split(" ")
                _logger.info(
                    "\tIncluding file {} from {}@{}".format(fpath, new_remote, new_ref)
                )
                include_doc = fetch_include(fpath, new_ref, model_fp, new_remote)
                _logger.debug(f"FETCHED INCLUDE: \n{pformat(include_doc)}")
                include_doc = include_includes(include_doc, new_ref, model_fp, new_remote)
                _logger.debug(
                    f"FETCHED INCLUDE AFTER RESCURSIVE INCLUDE: \n{pformat(include_doc)}"
                )
                parsed_params.extend(include_doc)
        else:
            parsed_params.append(parameter)
    return parsed_params


@click.command()
@click.option(
    "-wd",
    "--use_work_dir",
    "--using-work-dir",
    "work_dir",
    is_flag=True,
    help="Use model files from current working directory instead of git",
)
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
    relpath = model_fn
    branch = confirm_git_branch(work_dir, nomitall)
    doc = fetch_git_yaml(relpath, branch)
    model_type = doc.get("type")
    doc.pop("docker", None)
    if not model_type:
        _logger.error("Model does not have a type, this is required")
        sys.exit(1)
    # add legacy model verison if it doesn't exit
    if model_type == "engine":
        for action, action_dict in doc["actions"].items():
            _logger.info("Parsing {}".format(action))
            action_dict["parameters"] = include_includes(
                action_dict["parameters"], branch, model_fn
            )
        try:
            image, tag = doc["location"]["image"].split(":")
        except ValueError:
            image = doc["location"]["image"]
        if nomitall == "nomitall-prod":
            tag = "prod"
        elif nomitall == "nomitall-stage":
            tag = "stage"
        else:
            tag = "stage"
        doc["location"]["image"] = ":".join([image, tag])
    else:
        doc["parameters"] = include_includes(doc["parameters"], branch, model_fn)

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
