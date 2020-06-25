import json
import urllib.parse

import requests
import agilicus

from . import context, response, token_parser


def _create_token(ctx, user_id, duration, aud, hosts=[], roles={}, org_id=None):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["Content-type"] = "application/json"

    data = {}
    data["sub"] = user_id
    data["time_validity"] = {"duration": duration}
    data["audiences"] = aud
    if hosts:
        data["hosts"] = hosts
    if org_id:
        data["org"] = org_id
    if roles:
        data["roles"] = roles

    response = requests.post(
        context.get_api(ctx) + "/v1/tokens",
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    return response


def get_introspect(ctx, raw_token, exclude_roles, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    options = agilicus.TokenIntrospectOptions(exclude_roles=exclude_roles)
    token_obj = agilicus.TokenIntrospect(token=raw_token, introspect_options=options)
    resp = apiclient.tokens_api.create_introspect_token(token_obj, **kwargs)
    return resp


def get_token(ctx, user_id, org_id, duration, hosts):
    token = context.get_token(ctx)

    if not org_id:
        tok = token_parser.Token(token)
        if tok.hasRole("urn:api:agilicus:traffic-tokens", "owner"):
            org_id = tok.getOrg()

    hosts = json.loads(hosts)
    aud = [
        "urn:api:agilicus:gateway",
        "urn:api:agilicus:users",
        "urn:api:agilicus:applications",
    ]
    return _create_token(
        ctx, user_id, duration, aud=aud, hosts=hosts, org_id=org_id
    ).text


def create_token(ctx, user_id, roles, duration, audiences, org_id):
    result = _create_token(
        ctx, user_id, duration, aud=audiences, roles=roles, org_id=org_id
    )
    if result.status_code != 200:
        print("Unable to retrieve token: %i" % result.status_code)
        print(result.text)
        return None
    return result.text


def query_tokens(
    ctx,
    limit=None,
    expired_from=None,
    expired_to=None,
    issued_from=None,
    issued_to=None,
    org_id=None,
    jti=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    params = {}
    if limit:
        params["limit"] = limit
    if expired_from:
        params["exp_from"] = expired_from
    if expired_to:
        params["exp_to"] = expired_to
    if issued_from:
        params["iat_from"] = issued_from
    if issued_to:
        params["iat_to"] = issued_to
    if jti:
        params["jti"] = jti
    params["sub"] = "iqms2wHxqj6deKQ2s69wQH"
    if org_id:
        params["org"] = org_id
    else:
        org_id = context.get_org_id(ctx, token)
        if org_id:
            params["org"] = org_id

    query = urllib.parse.urlencode(params)
    uri = "/v1/tokens?{}".format(query)
    resp = requests.get(
        context.get_api(ctx) + uri, headers=headers, verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text
