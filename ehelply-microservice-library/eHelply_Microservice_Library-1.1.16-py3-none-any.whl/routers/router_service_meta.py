from fastapi import APIRouter, Cookie, Depends, Body, Query
from ehelply_bootstrapper.drivers.fast_api_utils.responses import *

from typing import List, Dict

import json
from pathlib import Path

from ehelply_bootstrapper.utils.state import State

router = APIRouter()


@router.get(
    '/meta',
    tags=["meta"],
)
async def get_meta():
    """
    Returns the service meta for this microservice
    :return:
    """
    return http_200_ok({
        "name": State.bootstrapper.service_meta.name,
        "summary": State.bootstrapper.service_meta.summary,
        "authors": State.bootstrapper.service_meta.authors,
        "author_emails": State.bootstrapper.service_meta.author_emails
    })


@router.get(
    '/releases',
    tags=["releases"],
)
async def get_releases():
    """
    Returns the release history of this microservice
    :return:
    """
    releases_path: Path = Path(Path(__file__).resolve().parents[3]).joinpath("releases.json")

    with open(str(releases_path)) as file:
        releases_data: list = json.load(file)

    return http_200_ok(releases_data)


@router.get(
    '/releases/{release}',
    tags=["releases"],
)
async def get_release(
        release: str
):
    """
    Returns information about a particular release
    :param release:
    :return:
    """
    releases_path: Path = Path(Path(__file__).resolve().parents[3]).joinpath("releases.json")

    with open(str(releases_path)) as file:
        releases_data: list = json.load(file)

    for release_from_service in releases_data:
        if release_from_service['version'] == release:
            return http_200_ok(release_from_service)

    return http_404_not_found()


@router.get(
    '/template',
    tags=["releases"],
)
async def get_service_template_details():
    """
    Returns details about the current service template this microservice is using such as the version
    :return:
    """
    package_path: Path = Path(Path(__file__).resolve().parents[3]).joinpath("ehelply-package.json")

    with open(str(package_path)) as file:
        package_data: dict = json.load(file)

    return package_data
