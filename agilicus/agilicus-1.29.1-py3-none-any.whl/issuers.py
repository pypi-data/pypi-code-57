import agilicus

from . import context
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import update_if_not_none
from .input_helpers import pop_item_if_none


def _build_updated_issuer(issuer, new_values):
    issuer_dict = issuer.to_dict()
    update_if_not_none(issuer_dict, new_values)

    # The clients aren't needed for updates
    issuer_dict.pop("clients", None)

    oidc_upstreams = issuer_dict.get("oidc_upstreams", [])
    for upstream in oidc_upstreams:
        pop_item_if_none(upstream)

    return agilicus.Issuer(**issuer_dict)


def _get_issuer(ctx, id, client, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    issuer = client.issuers_api.get_issuer(id, org_id=org_id)

    return issuer


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.issuers_api.list_issuers(**kwargs)
    if query_results:
        return query_results.issuer_extensions
    return


def show(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return _get_issuer(ctx, issuer_id, apiclient, **kwargs).to_dict()


def add(ctx, issuer, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer_model = agilicus.Issuer(issuer=issuer, org_id=org_id)
    return apiclient.issuers_api.create_issuer(issuer_model).to_dict()


def _update_issuer(ctx, issuer_id, updater, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    issuer = _build_updated_issuer(issuer, kwargs)

    return updater(apiclient.issuers_api, issuer_id, issuer).to_dict()


def update_root(ctx, issuer_id, **kwargs):
    return _update_issuer(ctx, issuer_id, agilicus.IssuersApi.replace_root, **kwargs)


def update_extension(ctx, issuer_id, **kwargs):
    return _update_issuer(ctx, issuer_id, agilicus.IssuersApi.replace_issuer, **kwargs)


def delete(ctx, issuer_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.delete_root(issuer_id, **kwargs)


def update_managed_upstreams(ctx, issuer_id, name, status, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.managed_upstreams:
        if upstream.name == name:
            upstream.enabled = status
            return apiclient.issuers_api.replace_issuer(
                issuer_id, issuer, **kwargs
            ).to_dict()
    print(f"{name} is not a managed upstream. Options are:")
    print([x.name for x in issuer.managed_upstreams])
    return


def update_oidc_upstreams(
    ctx,
    issuer_id,
    name,
    issuer_uri,
    client_id,
    client_secret,
    issuer_external_host,
    username_key,
    email_key,
    email_verification_required,
    request_user_info,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.oidc_upstreams:
        if upstream.name == name:
            if issuer_uri is not None:
                upstream.issuer = issuer_uri
            if client_id is not None:
                upstream.client_id = client_id
            if client_secret is not None:
                upstream.client_secret = client_secret
            if issuer_external_host is not None:
                upstream.issuer_external_host = issuer_external_host
            if username_key is not None:
                upstream.username_key = username_key
            if email_key is not None:
                upstream.email_key = email_key
            if email_verification_required is not None:
                upstream.email_verification_required = email_verification_required
            if request_user_info is not None:
                upstream.request_user_info = request_user_info
            return apiclient.issuers_api.replace_issuer(
                issuer_id, issuer, **kwargs
            ).to_dict()
    print(f"{name} is not an oidc upstream")
    return


def add_oidc_upstreams(
    ctx,
    issuer_id,
    name,
    issuer_uri,
    client_id,
    client_secret,
    issuer_external_host,
    username_key,
    email_key,
    email_verification_required,
    request_user_info,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    upstream = agilicus.OIDCUpstreamIdentityProvider(
        name,
        issuer_uri,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        email_key,
        email_verification_required,
        request_user_info,
    )
    issuer.oidc_upstreams.append(upstream)
    return apiclient.issuers_api.replace_issuer(issuer_id, issuer, **kwargs).to_dict()


def delete_oidc_upstreams(ctx, issuer_id, name, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    issuer = _get_issuer(ctx, issuer_id, apiclient, **kwargs)

    if not issuer:
        print(f"Cannot find issuer {issuer_id}")
        return

    for upstream in issuer.oidc_upstreams:
        if upstream.name == name:
            issuer.oidc_upstreams.remove(upstream)
            apiclient.issuers_api.replace_issuer(issuer_id, issuer, **kwargs)
            return

    print(f"{name} is not an oidc upstream")
    return


def query_clients(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    query_results = apiclient.issuers_api.list_clients(**kwargs)
    if query_results:
        return query_results.clients
    return


def show_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.get_client(client_id, **kwargs).to_dict()


def add_client(
    ctx, issuer_id, name, **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    client_model = agilicus.IssuerClient(issuer_id=issuer_id, name=name, **kwargs)
    return apiclient.issuers_api.create_client(client_model).to_dict()


def _get_client(ctx, apiclient, client_id, **kwargs):
    apiclient = context.get_apiclient(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    client = apiclient.issuers_api.get_client(client_id, org_id=org_id)

    # Note: the api raises a 404 if it's not found

    return client


def update_client(
    ctx, client_id, **kwargs,
):
    apiclient = context.get_apiclient(ctx)
    client = _get_client(ctx, apiclient, client_id, **kwargs)

    client_dict = client.to_dict()
    update_if_not_none(client_dict, kwargs)
    client_model = agilicus.IssuerClient(**client_dict)
    return apiclient.issuers_api.replace_client(client_id, client_model).to_dict()


def delete_client(ctx, client_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.issuers_api.delete_client(client_id, **kwargs)


def _add_to_client_list_and_replace(ctx, client_id, list_name, value, **kwargs):
    apiclient = context.get_apiclient(ctx)

    client = _get_client(ctx, apiclient, client_id, **kwargs)
    items = getattr(client, list_name) or []
    if value in items:
        return client.to_dict()

    items.append(value)
    setattr(client, list_name, items)
    return apiclient.issuers_api.replace_client(client.id, client).to_dict()


def _remove_from_client_list_and_replace(ctx, client_id, list_name, value, **kwargs):
    apiclient = context.get_apiclient(ctx)

    client = _get_client(ctx, apiclient, client_id, **kwargs)
    items = getattr(client, list_name) or []
    if value not in items:
        return client.to_dict()

    items.remove(value)
    setattr(client, list_name, items)
    return apiclient.issuers_api.replace_client(client.id, client).to_dict()


def add_redirect(ctx, client_id, redirect_url, **kwargs):
    return _add_to_client_list_and_replace(
        ctx, client_id, "redirects", redirect_url, **kwargs
    )


def delete_redirect(ctx, client_id, redirect_url, **kwargs):
    return _remove_from_client_list_and_replace(
        ctx, client_id, "redirects", redirect_url, **kwargs
    )


def add_restricted_organisation(ctx, client_id, restricted_org_id, **kwargs):
    return _add_to_client_list_and_replace(
        ctx, client_id, "restricted_organisations", restricted_org_id, **kwargs
    )


def delete_restricted_organisation(ctx, client_id, restricted_org_id, **kwargs):
    return _remove_from_client_list_and_replace(
        ctx, client_id, "restricted_organisations", restricted_org_id, **kwargs
    )
