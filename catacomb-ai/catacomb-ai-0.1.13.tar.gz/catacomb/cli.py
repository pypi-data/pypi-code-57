import os
import click
import requests
import docker
import urllib.request
import yaml
from .static import DOCKERFILE, SERVER
from .docker_logic import build, push, start

@click.group()
def cli():
    pass

cli.add_command(build, name="build")
cli.add_command(push, name="push")
cli.add_command(start, name="start")
