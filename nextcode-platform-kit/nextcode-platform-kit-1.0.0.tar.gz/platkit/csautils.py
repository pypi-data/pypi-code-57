#!/usr/bin/env python
"""
Authorize user access to project against CSA
"""
import logging
import requests
from http import HTTPStatus
from posixpath import join as urljoin
from platkit.config import Config

log = logging.getLogger("platkit")
config = Config()


def has_access_to_project(user, project):
    """
    Authorize method to check if user has access to given project
    Returns True if user has access to project and False otherwise.
    """
    csa_api_url = config.get("CSA_API_URL")
    csa_auth_user = config.get("CSA_API_USER")
    csa_auth_pass = config.get("CSA_API_PASS")
    if not csa_api_url or not csa_auth_user or not csa_auth_pass:
        raise KeyError("Missing config value CSA_API_URL or CSA_API_USER or CSA_API_PASS")

    csa_auth_url = urljoin(csa_api_url, "projects/{project_name}/users/{user_email}")

    url = csa_auth_url.format(project_name=project, user_email=user)
    log.info(
        "authorizing user '%s' in project '%s' using url %s with auth user '%s'",
        user,
        project,
        url,
        csa_auth_user,
    )
    rsp = None
    try:
        rsp = requests.get(url, auth=(csa_auth_user, csa_auth_pass))
        # we start by extracting the json so that non-json 404's will bubble up as exceptions
        data = rsp.json()
        if rsp.status_code == HTTPStatus.NOT_FOUND:
            return False
        rsp.raise_for_status()

    except Exception as ex:
        log.error("Can not reach CSA on %s for authorization: %s", url, ex)
        if rsp:
            log.error("Response: %s (code %s)", rsp.text, rsp.status_code)
        raise

    log.debug("CSA response from %s: %s - %s", url, rsp.status_code, data)

    if rsp.status_code == HTTPStatus.NOT_FOUND:
        return False
    else:
        return rsp.json()["access"]
