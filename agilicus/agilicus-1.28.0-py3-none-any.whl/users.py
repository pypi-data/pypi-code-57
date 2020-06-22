import json
import urllib.parse

import requests

from . import context, response, token_parser

USERS_BASE_URI = "/users"
GROUPS_BASE_URI = "/v1/groups"


def get_uri(type):
    if "user" == type:
        return USERS_BASE_URI
    elif "group" == type:
        return GROUPS_BASE_URI
    elif "sysgroup" == type:
        return GROUPS_BASE_URI
    elif "bigroup" == type:
        return GROUPS_BASE_URI


def query(
    ctx, org_id=None, type="user", email=None, previous_email=None, limit=None, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    params = {}

    if not org_id:
        tok = token_parser.Token(token)
        if tok.hasRole("urn:api:agilicus:users", "owner"):
            org_id = tok.getOrg()
    params["type"] = type
    if org_id:
        params["org_id"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org_id"] = org_id

    if email:
        params["email"] = email
    if previous_email:
        params["previous_email"] = previous_email
    if limit:
        params["limit"] = limit

    return apiclient.user_api.list_users(**params).to_dict()


def _get_user(ctx, user_id, org_id, type="user"):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}
    params["org_id"] = org_id

    query = urllib.parse.urlencode(params)
    uri = "{}/{}?{}".format(get_uri(type), user_id, query)
    resp = requests.get(
        context.get_api(ctx) + uri, headers=headers, verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp


def _update_if_present(object: dict, key, **kwargs):
    value = kwargs.get(key, None)
    if value is not None:
        object[key] = value


def get_user(ctx, user_id, org_id=None, type="user"):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    return _get_user(ctx, user_id, org_id, type).text


def add_user_role(ctx, user_id, application, roles):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    data = {}
    apps = {}
    apps[application] = roles
    data["roles"] = apps
    data["org_id"] = context.get_org_id(ctx, token)
    params = {}
    params["org_id"] = context.get_org_id(ctx, token)
    query = urllib.parse.urlencode(params)

    uri = "{}/{}/roles?{}".format(get_uri("user"), user_id, query)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def list_user_roles(ctx, user_id, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    params = {}
    params["org_id"] = org_id
    query = urllib.parse.urlencode(params)
    uri = "{}/{}/render_roles?{}".format(get_uri("user"), user_id, query)
    resp = requests.get(
        context.get_api(ctx) + uri, headers=headers, verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def delete_user(ctx, user_id, org_id=None, type="user"):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    uri = "/v1/orgs/{}/users/{}".format(org_id, user_id)
    resp = requests.delete(
        context.get_api(ctx) + uri, headers=headers, verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def add_group(ctx, first_name, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    user = {}
    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    user["org_id"] = org_id

    user["first_name"] = first_name

    uri = "{}".format(get_uri("group"))
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(user),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def add_group_member(ctx, group_id, member, org_id=None, member_org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    for id in member:
        member = {}
        member["id"] = id
        member["org_id"] = org_id
        if member_org_id:
            member["member_org_id"] = member_org_id
        uri = "{}/{}/members".format(get_uri("group"), group_id)
        resp = requests.post(
            context.get_api(ctx) + uri,
            headers=headers,
            data=json.dumps(member),
            verify=context.get_cacert(ctx),
        )
        response.validate(resp)


def delete_group_member(ctx, group_id, member, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    params = {}
    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    params = {}
    params["org_id"] = org_id
    query = urllib.parse.urlencode(params)
    for id in member:
        uri = "{}/{}/members/{}?{}".format(get_uri("group"), group_id, id, query)
        resp = requests.delete(
            context.get_api(ctx) + uri,
            headers=headers,
            data=json.dumps(member),
            verify=context.get_cacert(ctx),
        )
        response.validate(resp)


def add_user(ctx, first_name, last_name, email, org_id, **kwargs):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    user = {}
    user["org_id"] = org_id
    user["first_name"] = first_name
    user["last_name"] = last_name
    user["email"] = email
    _update_if_present(user, "external_id", **kwargs)

    uri = "/users"
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(user),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def update_user(ctx, user_id, org_id, **kwargs):
    token = context.get_token(ctx)

    if org_id is None:
        org_id = context.get_org_id(ctx, token)

    user = _get_user(ctx, user_id, org_id, "user").json()
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    _update_if_present(user, "first_name", **kwargs)
    _update_if_present(user, "last_name", **kwargs)
    _update_if_present(user, "email", **kwargs)
    _update_if_present(user, "external_id", **kwargs)
    _update_if_present(user, "auto_created", **kwargs)

    # Remove read-only values
    user.pop("updated", None)
    user.pop("created", None)
    user.pop("member_of", None)
    user.pop("id", None)
    user.pop("organisation", None)
    user.pop("type", None)

    uri = f"/users/{user_id}"
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(user),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return _get_user(ctx, user_id, org_id, "user").json()
