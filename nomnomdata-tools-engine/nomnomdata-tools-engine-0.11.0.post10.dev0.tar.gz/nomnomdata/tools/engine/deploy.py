import logging
import sys
from os import chdir, path
from urllib.parse import urljoin

import click
import docker
import requests
import yaml
from compose.progress_stream import stream_output

from nomnomdata.auth import NNDAuth

_logger = logging.getLogger(__name__)


class NomitallSession(requests.Session):
    def __init__(self, prefix_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        _logger.info(f"Request {method}:{url}")
        return super().request(method, url, *args, **kwargs)


@click.command(name="deploy")
@click.option(
    "-p",
    "--path",
    "buildp",
    default=".",
    show_default=True,
    help="Docker build context path",
)
@click.option(
    "-f",
    "--model-file",
    "mpath",
    default="./",
    help="Path to the engine model.yaml to build, if this is a folder model.yaml will be assumed to be in there "
    "Examples: nomnom/test/waittask/model.yaml",
)
@click.option(
    "-d",
    "--docker-file",
    "dpath",
    default="./",
    help="Path to the engine dockerfile to build, if this is a folder Dockerfile will be assumed to be in there "
    "Examples: nomnom/test/waittask/engine.dockerfile",
)
@click.option(
    "-n",
    "--nomitall",
    default="nomitall-stage",
    help="Specify the nomitall to update [nomitall-prod,nomitall-stage,custom_url]",
)
@click.option("--dry-run", is_flag=True, help="Build engine but do not deploy")
@click.pass_context
def deploy(ctx, buildp, mpath, dpath, nomitall, dry_run):
    "Build engine docker images and optionally run tests."
    if nomitall == "nomitall-prod":
        nomitall_url = "https://user.api.nomnomdata.com/api/1/"
        tag = "prod"
    elif nomitall == "nomitall-stage":
        nomitall_url = "https://staging.user.api.nomnomdata.com/api/1/"
        tag = "stage"
    else:
        nomitall_url = nomitall
        tag = "stage"
    chdir(buildp)
    if path.isdir(mpath):
        mpath = path.join(mpath, "model.yaml")
    if path.isdir(dpath):
        dpath = path.join(dpath, "Dockerfile")
    engine_model = yaml.full_load(open(mpath))
    engine_uuid = engine_model["uuid"]

    session = NomitallSession(prefix_url=nomitall_url)
    session.auth = NNDAuth()
    resp = session.request("get", f"engine/create-deploy-token/{engine_uuid}")
    data = resp.json()
    engine_name = data["repoUrl"]
    client = docker.from_env()
    try:
        client.ping()
    except (requests.ConnectionError, docker.errors.APIError) as e:
        raise Exception(
            "There was a problem connecting to the docker agent, ensure it is running and in a good state"
        ) from e
    image = build_engine(
        engine_name=engine_name, client=client, tag=tag, docker_file=dpath,
    )
    if not dry_run:
        deploy_engine(image, data)


def deploy_engine(image, creds):
    _logger.info("----Pushing image----")
    client = docker.from_env()
    client.login(
        username=creds["user"],
        password=creds["token"],
        registry=creds["registryUrl"],
        reauth=True,
    )
    push_logs = client.api.push(image, stream=True)
    list(stream_output(push_logs, sys.stdout))
    _logger.info("----Successfully pushed image----")


def build_engine(engine_name, client, tag, docker_file, buildargs=None):
    _logger.info("----Building image----")
    build_logs = client.api.build(
        dockerfile=docker_file,
        tag=":".join([engine_name, tag]),
        rm=True,
        path=".",
        pull=True,
        buildargs=buildargs,
    )
    list(stream_output(build_logs, sys.stdout))
    _logger.info("----Finished building image----")
    return ":".join([engine_name, tag])
