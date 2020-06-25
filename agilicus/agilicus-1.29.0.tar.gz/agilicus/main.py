import json
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import click
import jwt
from click_shell import shell
from prettytable import PrettyTable

from . import (
    apps,
    audits,
    challenges,
    context,
    credentials,
    catalogues,
    csv_rules,
    env_config,
    files,
    gateway,
    issuers,
    logs,
    metrics,
    orgs,
    permissions,
    scopes,
    tokens,
    users,
    whoami,
)


def prompt(ctx):
    issuer_host = urlparse(context.get_issuer(ctx)).netloc
    org = context.get_org(ctx)
    if not org:
        return f"{issuer_host}$ "
    return f"{issuer_host}/{org['organisation']}$ "


def app_completion(ctx, args, incomplete):
    context.setup(ctx)
    _apps = apps.query(ctx, None)
    results = []
    for _app in _apps:
        if incomplete in _app["name"]:
            results.append(_app["name"])
    return results


def env_completion(ctx, args, incomplete):
    context.setup(ctx)
    _envs = apps.env_query(ctx, None, args.pop())
    results = []
    for _env in _envs:
        if incomplete in _env["name"]:
            results.append(_env["name"])
    return results


def user_completion(ctx, args, incomplete):
    context.setup(ctx)
    _users = users.query(ctx)["users"]
    results = []
    for _user in _users:
        if incomplete in _user["email"]:
            results.append(_user["email"])
    return results


def sub_org_completion(ctx, args, incomplete):
    context.setup(ctx)
    suborgs = orgs.query_suborgs(ctx)
    results = []
    for suborg in suborgs:
        if incomplete in suborg["organisation"]:
            results.append(suborg["organisation"])
    return results


def get_user_id_from_email(ctx, email, org_id=None):
    _users = users.query(ctx, email=email, org_id=org_id)["users"]
    if len(_users) == 1:
        return _users[0]
    print(f"Cannot find user email:{email}")


# @click.group()
@shell(prompt=prompt)
@click.option("--token", default=None)
@click.option("--api", default=context.API_DEFAULT)
@click.option("--cacert", default=context.CACERT_DEFAULT)
@click.option("--client_id", default=context.CLIENT_ID_DEFAULT)
@click.option("--issuer", default=context.ISSUER_DEFAULT)
@click.option("--auth_local_webserver/--noauth_local_webserver", default=True)
@click.option("--org_id", default=context.ORG_ID_DEFAULT)
@click.option("--header", default=context.HEADER_DEFAULT, type=bool)
@click.option("--scope", default=scopes.get_default_scopes(), multiple=True)
@click.option("--admin", is_flag=True)
@click.pass_context
def cli(
    ctx,
    token,
    api,
    cacert,
    client_id,
    issuer,
    auth_local_webserver,
    org_id,
    header,
    scope,
    admin,
):
    ctx.ensure_object(dict)
    ctx.obj["TOKEN"] = token
    ctx.obj["API"] = api
    ctx.obj["CACERT"] = cacert
    ctx.obj["CLIENT_ID"] = client_id
    ctx.obj["ISSUER"] = issuer
    ctx.obj["AUTH_LOCAL_WEBSERVER"] = auth_local_webserver
    ctx.obj["ORG_ID"] = org_id
    ctx.obj["HEADER"] = header
    ctx.obj["SCOPES"] = list(scope)
    ctx.obj["ADMIN_MODE"] = admin
    if admin:
        # Extend the provided scopes (either default or chosen by user) with the admin
        # ones.
        ctx.obj["SCOPES"].extend(scopes.get_admin_scopes())
    context.save(ctx)

    token = whoami.whoami(ctx, False)
    org_id = context.get_org_id(ctx, token)
    if org_id:
        org = orgs.get(ctx, org_id)
        ctx.obj["ORGANISATION"] = org
    return None


@cli.command(name="use-org")
@click.pass_context
@click.argument("organisation", default=None, autocompletion=sub_org_completion)
def use_org(ctx, organisation):
    org_list = orgs.query_suborgs(ctx, organisation=organisation)
    found_org = None
    for _org in org_list:
        if _org["organisation"] == organisation:
            found_org = _org

    if not found_org:
        print(f"No sub organisation found named {organisation}")
        return

    org_id = found_org["id"]
    ctx.obj["ORG_ID"] = org_id

    token = whoami.whoami(ctx, False)
    if token:
        ctx.obj["ORGANISATION"] = found_org
    context.save(ctx)


def output_tokens_list(tokens_list):
    table = PrettyTable(
        ["jti", "roles", "iat", "exp", "aud", "user", "session", "revoked"]
    )
    for token in tokens_list:
        table.add_row(
            [
                token["jti"],
                json.dumps(token["roles"], indent=2),
                token["iat"],
                token["exp"],
                json.dumps(token["aud"], indent=2),
                token["sub"],
                token["session"],
                token["revoked"],
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="delete-credentials")
@click.pass_context
def _delete_credentials(ctx, **kwargs):
    credentials.delete_credentials_with_ctx(ctx)


@cli.command(name="list-tokens")
@click.option("--limit", default=None)
@click.option("--expired-from", default=None)
@click.option("--expired-to", default=None)
@click.option("--issued-from", default=None)
@click.option("--issued-to", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def list_tokens(ctx, org_id, **kwargs):
    output_tokens_list(
        json.loads(tokens.query_tokens(ctx, org_id=org_id, **kwargs))["tokens"]
    )


@cli.command(name="get-token")
@click.argument("user_id", default=None)
@click.option("--duration", default=3600, prompt=True)
@click.option(
    "--hosts",
    default='[{"upstream_host": "example.com", "allowed_list": [{"methods" : ["get"], "paths" : ["/.*"]}]}]',  # noqa
    prompt=True,
)
@click.pass_context
def token_get(ctx, user_id, duration, hosts, **kwargs):
    user = json.loads(users.get_user(ctx, user_id))
    token = tokens.get_token(ctx, user_id, user["org_id"], duration, hosts, **kwargs)
    output_entry(jwt.decode(token, verify=False))
    print(token)


def output_gw_audit_list(audit_list):
    table = PrettyTable(["time", "authority", "token_id"])
    for entry in audit_list:
        table.add_row([entry["time"], entry["authority"], entry["token_id"]])
    table.align = "l"
    print(table)


@cli.command(name="gateway-audit")
@click.option("--limit", default=None)
@click.option("--token-id", default=None)
def gateway_audit(**kwargs):
    output_gw_audit_list(json.loads(gateway.query_audit(**kwargs)))


@cli.command(name="list-audit-records")
@click.option("--limit", type=int, default=50)
@click.option("--org_id", default=None)
@click.option("--dt_from", default=None)
@click.option("--dt_to", default=None)
@click.option("--user_id", default=None)
@click.option("--action", default=None)
@click.option("--target_id", default=None)
@click.option("--token_id", default=None)
@click.option("--api_name", default=None)
@click.option("--target_resource_type", default=None)
@click.pass_context
def list_audit_records(ctx, **kwargs):
    records = audits.query(ctx, **kwargs)
    print(audits.format_audit_list_as_text(records))


def output_list_users(orgs_by_id, users_list):
    table = PrettyTable(
        ["id", "First Name", "Last Name", "Email", "External_ID", "Organisation",]
    )
    for entry in users_list:
        org_name = "none"

        org_id = entry.get("org_id", None)
        if org_id and org_id in orgs_by_id:
            org_name = orgs_by_id[entry["org_id"]]["organisation"]

        table.add_row(
            [
                entry["id"],
                entry["first_name"],
                entry.get("last_name", ""),
                entry["email"],
                entry.get("external_id", ""),
                org_name,
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="list-users")
@click.option("--organisation", default=None)
@click.option("--org_id", default=None)
@click.option("--email", default=None)
@click.option("--previous_email", default=None)
@click.option("--limit", type=int, default=None)
@click.pass_context
def list_users(ctx, organisation, org_id, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))

    output_list_users(org_by_id, users.query(ctx, org_id, **kwargs)["users"])


def output_entry(entry):
    table = PrettyTable(["field", "value"])
    for k, v in list(entry.items()):
        if k == "nbf" or k == "exp" or k == "iat":
            _t = datetime.fromtimestamp(v, timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S %z (%Z)"
            )  # noqa
            table.add_row([k, json.dumps(_t, indent=4)])
        elif k == "created" or k == "updated":
            table.add_row([k, v])
        else:
            table.add_row([k, json.dumps(v, indent=4, default=str)])
    table.align = "l"
    print(table)


@cli.command(name="show-user")
@click.argument("email", autocompletion=user_completion)
@click.option("--org_id", default=None)
@click.pass_context
def show_user(ctx, email, org_id):
    _user = get_user_id_from_email(ctx, email, org_id)
    if _user:
        output_entry(json.loads(users.get_user(ctx, _user["id"], org_id)))


@cli.command(name="add-user")
@click.argument("first-name")
@click.argument("last_name")
@click.argument("email")
@click.argument("org_id")
@click.option("--external-id", default=None)
@click.pass_context
def add_user(ctx, first_name, last_name, email, org_id, **kwargs):
    output_entry(users.add_user(ctx, first_name, last_name, email, org_id, **kwargs))


@cli.command(name="update-user")
@click.argument("email", autocompletion=user_completion)
@click.option("--org_id", default=None)
@click.option("--email", default=None)
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--external-id", default=None)
@click.option("--auto_created", type=bool, default=None)
@click.pass_context
def update_user(ctx, email, org_id, **kwargs):
    _user = get_user_id_from_email(ctx, email, org_id)
    if _user:
        output_entry(
            users.update_user(ctx, user_id=_user["id"], org_id=org_id, **kwargs)
        )


@cli.command(name="delete-user")
@click.argument("email", autocompletion=user_completion)
@click.pass_context
def delete_user(ctx, email):
    _user = get_user_id_from_email(ctx, email)
    if _user:
        users.delete_user(ctx, _user["id"])


@cli.command(name="add-user-role")
@click.argument("email", autocompletion=user_completion)
@click.argument("application", autocompletion=app_completion)
@click.option("--role", multiple=True)
@click.pass_context
def add_user_role(ctx, email, application, role):
    _user = get_user_id_from_email(ctx, email)
    if _user:
        roles = []
        for _role in role:
            roles.append(_role)
        users.add_user_role(ctx, _user["id"], application, roles)
        output_entry(json.loads(users.get_user(ctx, _user["id"])))


@cli.command(name="list-user-roles")
@click.argument("email", autocompletion=user_completion)
@click.option("--org_id", default=None)
@click.pass_context
def list_user_role(ctx, email, org_id):
    _user = get_user_id_from_email(ctx, email, org_id)
    if _user:
        roles = json.loads(users.list_user_roles(ctx, _user["id"], org_id))
        table = PrettyTable(["application/service", "roles"])
        table.align = "l"
        for app, rolelist in roles.items():
            table.add_row([app, rolelist])
        print(table)


def output_list_orgs(orgs_list):
    table = PrettyTable(["id", "Organisation", "issuer", "subdomain"])
    for entry in orgs_list:
        subdomain = entry.get("subdomain", None)
        if "subdomain" not in entry:
            subdomain = None
        table.add_row([entry["id"], entry["organisation"], entry["issuer"], subdomain])
    table.align = "l"
    print(table)


def output_list_groups(orgs_by_id, groups_list):
    table = PrettyTable(["id", "Email", "members"])
    for entry in groups_list:
        _members = []
        for _member in entry["members"]:
            _members.append(_member["email"])
        table.add_row(
            [entry["id"], entry["email"], "\n".join(_members),]
        )
    table.align = "l"
    print(table)


@cli.command(name="list-groups")
@click.option("--organisation", default=None)
@click.option("--org_id", default=None)
@click.option("--type", default="group")
@click.pass_context
def list_groups(ctx, organisation, org_id, type, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))

    output_list_groups(org_by_id, users.query(ctx, org_id, type, **kwargs)["groups"])


@cli.command(name="list-sysgroups")
@click.option("--organisation", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def list_sysgroups(ctx, organisation, org_id, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))

    output_list_groups(
        org_by_id, users.query(ctx, org_id, type="sysgroup", **kwargs)["groups"],
    )


@cli.command(name="add-group")
@click.argument("first-name")
@click.option("--org_id")
@click.pass_context
def add_group(ctx, first_name, org_id):
    output_entry(users.add_group(ctx, first_name, org_id))


@cli.command(name="add-group-member")
@click.argument("group_id", default=None)
@click.option("--org_id", default=None)
@click.option("--member_org_id", default=None)
@click.option("--member", multiple=True)
@click.pass_context
def add_group_member(ctx, group_id, org_id, member, member_org_id):
    users.add_group_member(ctx, group_id, member, org_id, member_org_id)


@cli.command(name="delete-group-member")
@click.argument("group_id", default=None)
@click.option("--member", multiple=True)
@click.option("--org_id", default=None)
@click.pass_context
def delete_group_member(ctx, group_id, org_id, member):
    users.delete_group_member(ctx, group_id, member, org_id)


@cli.command(name="delete-group")
@click.argument("group_id", default=None)
@click.pass_context
def delete_group(ctx, group_id):
    users.delete_user(ctx, group_id, type="group")


@cli.command(name="list-orgs")
@click.option("--org_id", default=None)
@click.option("--issuer", default=None)
@click.pass_context
def list_orgs(ctx, **kwargs):
    output_list_orgs(orgs.query(ctx, **kwargs))


@cli.command(name="list-sub-orgs")
@click.option("--org_id", default=None)
@click.pass_context
def list_sub_orgs(ctx, **kwargs):
    output_list_orgs(orgs.query_suborgs(ctx, **kwargs))


@cli.command(name="show-org")
@click.argument("org_id", default=None)
@click.pass_context
def show_org(ctx, org_id, **kwargs):
    output_entry(orgs.get(ctx, org_id, **kwargs))


@cli.command(name="update-org")
@click.argument("org_id", default=None)
@click.option("--auto_create", type=bool, default=None)
@click.option("--issuer", default=None)
@click.option("--issuer_id", default=None)
@click.option("--contact_id", default=None)
@click.option("--subdomain", default=None)
@click.option("--external_id", default=None)
@click.pass_context
def update_org(
    ctx,
    org_id,
    auto_create,
    issuer,
    issuer_id,
    contact_id,
    subdomain,
    external_id,
    **kwargs,
):
    orgs.update(
        ctx,
        org_id,
        auto_create=auto_create,
        issuer=issuer,
        issuer_id=issuer_id,
        contact_id=contact_id,
        subdomain=subdomain,
        external_id=external_id,
        **kwargs,
    )
    output_entry(orgs.get(ctx, org_id))


@cli.command(name="add-org")
@click.argument("organisation")
@click.argument("issuer")
@click.option("--issuer_id", default=None)
@click.option("--auto_create", type=bool, default=True)
@click.option("--contact_id", default=None)
@click.option("--subdomain", default=None)
@click.pass_context
def add_org(
    ctx, organisation, issuer, issuer_id, contact_id, auto_create, subdomain, **kwargs
):
    output_entry(
        orgs.add(
            ctx,
            organisation,
            issuer,
            issuer_id,
            contact_id,
            auto_create,
            subdomain=subdomain,
            **kwargs,
        )
    )


@cli.command(name="add-sub-org")
@click.argument("organisation")
@click.option("--auto_create", type=bool, default=True)
@click.option("--contact_id", default=None)
@click.option("--subdomain", default=None)
@click.pass_context
def add_sub_org(ctx, organisation, contact_id, auto_create, subdomain, **kwargs):
    output_entry(
        orgs.add_suborg(ctx, organisation, contact_id, auto_create, subdomain, **kwargs)
    )


@cli.command(name="delete-sub-org")
@click.argument("org_id")
@click.pass_context
def delete_sub_org(ctx, org_id):
    orgs.delete_suborg(ctx, org_id)


@cli.command(name="delete-org")
@click.argument("org_id", default=None)
@click.pass_context
def delete_org(ctx, org_id, **kwargs):
    orgs.delete(ctx, org_id, **kwargs)


def output_list_apps(orgs_by_id, apps_list):
    table = PrettyTable(["id", "Application", "Organisation"])
    for entry in apps_list:

        org_name = "none"
        org_id = entry.get("org_id", None)
        if org_id and org_id in orgs_by_id:
            org_name = orgs_by_id[org_id]["organisation"]

        table.add_row([entry["id"], entry["name"], org_name])
    table.align = "l"
    print(table)


@cli.command(name="list-applications")
@click.option("--organisation", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def list_applications(ctx, organisation, org_id, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))
    output_list_apps(org_by_id, apps.query(ctx, org_id, **kwargs))


@cli.command(name="list-environments")
@click.argument("application", autocompletion=app_completion)
@click.option("--organisation", default=None)
@click.option("--org_id", default=None)
@click.option("--filter", default=None)
@click.pass_context
def list_environments(ctx, organisation, org_id, filter, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))
    table = PrettyTable(
        ["Name", "Assignments", "Services"],
        header=context.header(ctx),
        border=context.header(ctx),
    )
    for env in apps.env_query(ctx, org_id, **kwargs):
        _services = []
        for service in env.get("application_services", []):
            _services.append(service["name"])
        table.add_row([env["name"], env["assignments"], _services])
    table.align = "l"
    if filter:
        print(table.get_string(fields=filter.split(",")))
    else:
        print(table)


@cli.command(name="list-application-services")
@click.option("--org_id", default=None)
@click.pass_context
def list_application_services(ctx, **kwargs):
    table = PrettyTable(
        [
            "id",
            "name",
            "hostname",
            "ipv4_addresses",
            "name_resolution",
            "port",
            "protocol",
        ]
    )
    services = apps.get_application_services(ctx, **kwargs)
    for obj in services:
        service = obj.to_dict()
        table.add_row(
            [
                service["id"],
                service["name"],
                service["hostname"],
                service["ipv4_addresses"],
                service["name_resolution"],
                service["port"],
                service["protocol"],
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="add-application-service")
@click.argument("name", default=None)
@click.argument("hostname", default=None)
@click.argument("port", type=int, default=None)
@click.option("--org_id", default=None)
@click.option("--ipv4_addresses", default=None)
@click.option("--name_resolution", default=None)
@click.option("--protocol", default=None)
@click.pass_context
def add_application_service(ctx, name, hostname, port, org_id, **kwargs):
    output_entry(
        apps.add_application_service(
            ctx, name, hostname, port, org_id=org_id, **kwargs
        ).to_dict()
    )


@cli.command(name="update-application-service")
@click.argument("id", default=None)
@click.option("--name", default=None)
@click.option("--hostname", default=None)
@click.option("--port", type=int, default=None)
@click.option("--org_id", default=None)
@click.option("--ipv4_addresses", default=None)
@click.option("--name_resolution", default=None)
@click.option("--protocol", default=None)
@click.pass_context
def update_application_service(ctx, id, **kwargs):
    output_entry((apps.update_application_service(ctx, id, **kwargs)))


@cli.command(name="add-application-service-assignment")
@click.argument("app_service_name", default=None)
@click.argument("app_name", default=None)
@click.argument("environment_name", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def add_application_service_assignment(ctx, **kwargs):
    output_entry(apps.add_application_service_assignment(ctx, **kwargs))


@cli.command(name="delete-application-service-assignment")
@click.argument("app_service_name", default=None)
@click.argument("app_name", default=None)
@click.argument("environment_name", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_application_service_assignment(ctx, **kwargs):
    apps.delete_application_service_assignment(ctx, **kwargs)


@cli.command(name="show-application-service")
@click.argument("id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_application_service(ctx, id, org_id, **kwargs):
    output_entry(
        apps.get_application_service(ctx, id, org_id=org_id, **kwargs).to_dict()
    )


@cli.command(name="delete-application-service")
@click.argument("name", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_application_service(ctx, name, org_id, **kwargs):
    print(apps.delete_application_service(ctx, name, org_id=org_id, **kwargs))


def output_environment_entries(entry):
    table = PrettyTable(["field", "value"])
    for k, v in list(entry.items()):
        table.add_row([k, v])
    table.align = "l"
    print(table)


@cli.command(name="show-environment")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.pass_context
def show_environment(ctx, application, env_name, org_id, **kwargs):
    output_environment_entries(
        apps.get_env(ctx, application, env_name, org_id, **kwargs)
    )


@cli.command(name="delete-environment")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.pass_context
def delete_environment(ctx, app_name, **kwargs):
    _app = _get_app(ctx, app_name, **kwargs)
    if _app:
        apps.delete_environment(ctx, app_id=_app["id"], **kwargs)


@cli.command(name="update-environment")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.option("--version_tag", default=None)
@click.option("--serverless_image", default=None)
@click.option("--config_mount_path", default=None)
@click.option("--config_as_mount", help="json string", default=None)
@click.option("--config_as_env", help="json string", default=None)
@click.option("--secrets_mount_path", default=None)
@click.option("--secrets_as_mount", default=None)
@click.option("--secrets_as_env", default=None)
@click.pass_context
def update_environment(
    ctx,
    app_name,
    env_name,
    org_id,
    version_tag,
    config_mount_path,
    config_as_mount,
    config_as_env,
    secrets_mount_path,
    secrets_as_mount,
    secrets_as_env,
    **kwargs,
):
    _app = _get_app(ctx, app_name, org_id=org_id)
    if _app:
        apps.update_env(
            ctx,
            _app["id"],
            env_name,
            org_id,
            version_tag,
            config_mount_path,
            config_as_mount,
            config_as_env,
            secrets_mount_path,
            secrets_as_mount,
            secrets_as_env,
            **kwargs,
        )


@cli.command(name="delete-application")
@click.argument("app_name", autocompletion=app_completion)
@click.option("--org_id", default=None)
@click.pass_context
def delete_application(ctx, app_name, **kwargs):
    _app = _get_app(ctx, app_name, **kwargs)
    if _app:
        apps.delete(ctx, _app["id"], **kwargs)


@cli.command(name="add-application")
@click.argument("name")
@click.argument("org_id")
@click.argument("category")
@click.pass_context
def add_application(ctx, name, org_id, category):
    output_entry(json.loads(apps.add(ctx, name, org_id, category)))


@cli.command(name="assign-application")
@click.argument("env_name")
@click.argument("app_id")
@click.argument("org_id")
@click.argument("assigned_org_id")
@click.option("--admin-org-id", default=None)
@click.pass_context
def assign_application(ctx, env_name, app_id, org_id, assigned_org_id, admin_org_id):
    output_entry(
        json.loads(
            apps.update_assignment(
                ctx,
                env_name,
                app_id,
                org_id,
                assigned_org_id,
                admin_org_id=admin_org_id,
            )
        )
    )


@cli.command(name="unassign-application")
@click.argument("env_name")
@click.argument("app_id")
@click.argument("org_id")
@click.argument("assigned_org_id")
@click.pass_context
def unassign_application(ctx, env_name, app_id, org_id, assigned_org_id):
    output_entry(
        json.loads(
            apps.update_assignment(
                ctx, env_name, app_id, org_id, assigned_org_id, unassign=True
            )
        )
    )


def _get_app(ctx, app_name, org_id=None, **kwargs):
    _app = apps.get_app(ctx, org_id, app_name)
    if _app:
        return _app
    else:
        print(f"Application '{app_name}' not found")


@cli.command(name="show-application")
@click.argument("app_name", autocompletion=app_completion)
@click.option("--org_id", default=None)
@click.pass_context
def show_application(ctx, app_name, **kwargs):
    _app = _get_app(ctx, app_name, **kwargs)
    if _app:
        output_entry(_app)


@cli.command(name="update-application")
@click.argument("app_name", autocompletion=app_completion)
@click.option("--image", default=None)
@click.option("--port", type=int, default=None)
@click.option("--org_id", default=None)
@click.pass_context
def update_application(ctx, app_name, org_id, **kwargs):
    _app = _get_app(ctx, app_name, org_id=org_id)
    if _app:
        apps.update_application(ctx, _app["id"], org_id, **kwargs)
        output_entry(json.loads(apps.get(ctx, _app["id"])))


@cli.command(name="add-role")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("role-name")
@click.pass_context
def add_role(ctx, app_name, role_name):
    _app = _get_app(ctx, app_name)
    if _app:
        apps.add_role(ctx, _app["id"], role_name)
        output_entry(json.loads(apps.get(ctx, _app["id"])))


@cli.command(name="rules-from-csv")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("role-name")
@click.option("--file-name", default="-")
@click.option("--org_id", default=None)
@click.option("--hostname", default=None)
@click.pass_context
def rules_from_csv(ctx, app_name, role_name, file_name, org_id, hostname):
    _app = _get_app(ctx, app_name, org_id=org_id)
    if _app:
        result = csv_rules.add_rules_to_app(
            ctx, _app["id"], role_name, file_name, org_id, hostname
        )
        output_entry(result)


@cli.command(name="add-definition")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("key")
@click.argument("json-path")
@click.pass_context
def add_definition(ctx, app_name, key, json_path):
    _app = _get_app(ctx, app_name)
    if _app:
        apps.add_definition(ctx, _app["id"], key, json_path)
        output_entry(json.loads(apps.get(ctx, _app["id"])))


@cli.command(name="add-rule")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("role-name")
@click.argument("method")
@click.argument("path-regex")
@click.option("--query-param", "-q", type=click.Tuple([str, str]), multiple=True)
@click.option("--json-pointer", "-j", type=click.Tuple([str, str]), multiple=True)
@click.option("--rule-name", default=None)
@click.option("--host", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def add_rule(
    ctx, app_name, role_name, method, path_regex, query_param, json_pointer, **kwargs,
):
    apps.add_rule(
        ctx,
        app_name,
        role_name,
        method,
        path_regex,
        query_param,
        json_pointer,
        **kwargs,
    )


@cli.command(name="list-rules")
@click.argument("app_name", autocompletion=app_completion)
@click.option("--org_id", default=None)
@click.pass_context
def list_rules(ctx, **kwargs):
    table = PrettyTable(
        ["role", "name", "host", "method", "path", "query_param", "json_body"]
    )
    for role in apps.get_roles(ctx, **kwargs):
        for rule in role.get("rules", []):
            body = rule.get("body", {})
            json_body = None
            if body:
                json_body = body.get("json", None)
            table.add_row(
                [
                    role["name"],
                    rule["name"],
                    rule.get("host", ""),
                    rule["method"],
                    rule["path"],
                    rule.get("query_parameters", None),
                    json_body,
                ]
            )
    table.align = "l"
    print(table)


# Rows is a list of dictonaries with the same keys
def _format_subtable_objs(rows):
    return _format_subtable([row.to_dict() for row in rows])


def _format_subtable(rows):
    if not rows:
        return None

    column_names = [k for k, _ in rows[0].items()]
    table = PrettyTable(column_names)
    table.align = "l"
    for row in rows:  # dict
        values = [v for _, v in row.items()]
        table.add_row(values)
    return table


@cli.command(name="list-app-rules")
@click.argument("app-id", default=None)
@click.option("--org_id", default=None)
@click.option("--scope", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_app_rules(ctx, app_id, **kwargs):
    app_rules = apps.list_app_rules(ctx, app_id, **kwargs)
    table = PrettyTable(
        [
            "app_id",
            "rule_id",
            "org_id",
            "scope",
            "rule_type",
            "methods",
            "path",
            "query_param",
            "json_body",
        ]
    )
    for rule in app_rules:
        spec = rule.spec
        cond = spec.condition
        table.add_row(
            [
                spec.app_id,
                rule.metadata.id,
                spec.org_id,
                spec.scope,
                cond.rule_type,
                cond.methods,
                cond.path_regex,
                _format_subtable_objs(cond.query_parameters),
                _format_subtable_objs(cond.body.json),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="list-combined-rules")
@click.option("--org_id", default=None)
@click.option("--scopes", default=None)
@click.option("--app_id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_combined_rules(ctx, **kwargs):
    rules = apps.list_combined_rules(ctx, **kwargs)
    table = PrettyTable(["app_id", "role_id", "role_name", "org_id", "scope", "rules"])
    for rule in rules:
        status = rule.status
        table.add_row(
            [
                status.app_id,
                status.role_id,
                status.role_name,
                status.org_id,
                status.scope,
                _format_subtable_objs(
                    [sub_rule.spec.condition for sub_rule in status.rules]
                ),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="add-http-rule")
@click.argument("app-id")
@click.argument("path-regex")
@click.argument("methods", nargs=-1)
@click.option("--rule_type", default="HttpRule")
@click.option("--comments", default=None)
@click.option("--org_id", default=None)
@click.option("--rule_scope", default=None)
@click.pass_context
def add_http_rule(ctx, app_id, **kwargs):
    result = apps.add_http_rule(ctx, app_id, **kwargs)
    output_entry(result)


@cli.command(name="show-rule-v2")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--org_id", default=None)
@click.pass_context
def show_rule_v2(ctx, app_id, rule_id, **kwargs):
    result = apps.show_rule_v2(ctx, app_id, rule_id, **kwargs)
    output_entry(result)


@cli.command(name="delete-rule-v2")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--org_id", default=None)
@click.pass_context
def delete_rule_v2(ctx, app_id, rule_id, **kwargs):
    apps.delete_rule_v2(ctx, app_id, rule_id, **kwargs)


@cli.command(name="update-http-rule")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--path_regex", default=None)
@click.option("--rule_type", default="HttpRule")
@click.option("--comments", default=None)
@click.option("--org_id", default=None)
@click.option("--rule_scope", default=None)
@click.pass_context
def update_http_rule(ctx, app_id, rule_id, **kwargs):
    result = apps.update_http_rule(ctx, app_id, rule_id, **kwargs)
    output_entry(result)


@cli.command(name="update-http-rule-methods")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--methods", multiple=True, default=[])
@click.option("--org_id", default=None)
@click.pass_context
def update_http_rule_methods(ctx, app_id, rule_id, methods, **kwargs):
    result = apps.update_http_rule(ctx, app_id, rule_id, methods=methods, **kwargs)
    output_entry(result)


@cli.command(name="update-http-rule-query-params")
@click.argument("app-id")
@click.argument("rule-id")
@click.option(
    "--query-param",
    "-q",
    type=click.Tuple([str, str]),
    multiple=True,
    default=[],
    help="A pair of strings representing the query parameter name, match value",
)
@click.option("--org_id", default=None)
@click.pass_context
def update_http_rule_query_params(ctx, app_id, rule_id, query_param, **kwargs):
    result = apps.update_http_rule(
        ctx, app_id, rule_id, query_params=query_param, **kwargs
    )
    output_entry(result)


@cli.command(name="update-http-rule-body-params")
@click.argument("app-id")
@click.argument("rule-id")
@click.option(
    "--body_param",
    "-bp",
    type=click.Tuple([str, str, str, str]),
    multiple=True,
    help="A tuple of strings representing the name, value to match against, match type, and json pointer path",  # noqa
)
@click.option("--org_id", default=None)
@click.pass_context
def update_http_rule_body_params(ctx, app_id, rule_id, body_param, **kwargs):
    result = apps.update_http_rule(
        ctx, app_id, rule_id, body_params=body_param, **kwargs
    )
    output_entry(result)


@cli.command(name="list-roles")
@click.argument("app-id", default=None)
@click.option("--org_id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_roles(ctx, app_id, **kwargs):
    roles = apps.list_roles(ctx, app_id, **kwargs)
    table = PrettyTable(["app_id", "role_id", "name", "org_id", "included_roles"])
    for role in roles:
        spec = role.spec
        table.add_row(
            [
                spec.app_id,
                role.metadata.id,
                spec.name,
                spec.org_id,
                _format_subtable_objs(spec.included),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="add-role-v2")
@click.argument("app-id", default=None)
@click.argument("name", default=None)
@click.option("--org_id", default=None)
@click.option("--comments", default=None)
@click.option("--included", multiple=True)
@click.pass_context
def add_role_v2(ctx, app_id, name, **kwargs):
    result = apps.add_role_v2(ctx, app_id, name, **kwargs)
    output_entry(result)


@cli.command(name="show-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_role(ctx, app_id, role_id, **kwargs):
    result = apps.show_role_v2(ctx, app_id, role_id, **kwargs)
    output_entry(result)


@cli.command(name="delete-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_role(ctx, app_id, role_id, **kwargs):
    apps.delete_role_v2(ctx, app_id, role_id, **kwargs)


@cli.command(name="update-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--name", default=None)
@click.option("--comments", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def update_role(ctx, app_id, role_id, **kwargs):
    result = apps.update_role_v2(ctx, app_id, role_id, **kwargs)
    output_entry(result)


@cli.command(name="update-role-includes")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--included", multiple=True, default=[])
@click.pass_context
def update_role_includes(ctx, app_id, role_id, included, **kwargs):
    result = apps.update_role_v2(ctx, app_id, role_id, included=included, **kwargs)
    output_entry(result)


@cli.command(name="list-roles-to-rules")
@click.argument("app-id", default=None)
@click.option("--org_id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_roles_to_rules(ctx, app_id, **kwargs):
    roles = apps.list_roles_to_rules(ctx, app_id, **kwargs)
    table = PrettyTable(["role_to_rule_id", "role_id", "rule_id", "org_id", "included"])
    for role in roles:
        spec = role.spec
        table.add_row(
            [role.metadata.id, spec.role_id, spec.rule_id, spec.org_id, spec.included]
        )

    table.align = "l"
    print(table)


@cli.command(name="add-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.argument("rule-id", default=None)
@click.option("--org_id", default=None)
@click.option("--included/--excluded", default=True)
@click.pass_context
def add_role_to_rule(ctx, app_id, role_id, rule_id, **kwargs):
    result = apps.add_role_to_rule(ctx, app_id, role_id, rule_id, **kwargs)
    output_entry(result)


@cli.command(name="show-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    result = apps.show_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)
    output_entry(result)


@cli.command(name="delete-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    apps.delete_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)


@cli.command(name="update-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org_id", default=None)
@click.option("--included/--excluded", default=True)
@click.pass_context
def update_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    result = apps.update_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)
    output_entry(result)


@cli.command(name="delete-rule")
@click.argument("app_name", autocompletion=app_completion)
@click.argument("role_name")
@click.argument("rule_name")
@click.option("--org_id", default=None)
@click.pass_context
def delete_rule(ctx, **kwargs):
    apps.delete_rule(ctx, **kwargs)


@cli.command(name="whoami")
@click.option("--refresh/--no-refresh", default=False)
@click.pass_context
def get_whoami(ctx, refresh=None, **kwargs):
    token = whoami.whoami(ctx, refresh, **kwargs)
    print("Token:")
    output_entry(jwt.decode(token, verify=False))
    # print("Whoami response data:")
    # output_entry(access.get_whoami_resp(ctx))


@cli.command(name="show-token-introspection")
@click.option("--refresh", default=False)
@click.option("--token", default=None)
@click.option("--exclude_roles", default=False, type=bool)
@click.pass_context
def show_token_introspection(
    ctx, refresh=None, token=None, exclude_roles=False, **kwargs
):
    my_token = token
    if not my_token:
        my_token = whoami.whoami(ctx, refresh, **kwargs)
    result = tokens.get_introspect(ctx, my_token, exclude_roles, **kwargs)
    print(result)


@cli.command(name="get-token")
@click.pass_context
def get_token(ctx, **kwargs):
    token = whoami.whoami(ctx, False, **kwargs)
    if not token:
        print("No token found", file=sys.stderr)
        sys.exit(1)

    print(token)


@cli.command(name="create-token")
@click.argument("user")
@click.argument("org_id", type=str)
@click.option("--role", "-r", type=click.Tuple([str, str]), multiple=True)
@click.option("--duration", type=int, default=3600)
@click.option("--aud", type=str, multiple=True)
@click.pass_context
def create_token(ctx, user, org_id, role, duration, aud):
    roles = {endpoint: role_name for endpoint, role_name in role}
    token = tokens.create_token(ctx, user, roles, duration, aud, org_id=org_id)
    if not token:
        sys.exit(1)

    print(token)


@cli.command(name="list-files")
@click.option("--org_id", default=None)
@click.option("--tag", default=None)
@click.pass_context
def list_files(ctx, **kwargs):
    _files = files.query(ctx, **kwargs)
    table = PrettyTable(["id", "name", "tag", "created", "last_accessed", "size"])
    table.align = "l"
    for _file in _files:
        table.add_row(
            [
                _file["id"],
                _file["name"],
                _file["tag"],
                _file["created"],
                _file["last_access"],
                _file["size"],
            ]
        )
    print(table)


@cli.command(name="upload-file")
@click.argument("filename", type=click.Path(exists=True))
@click.option("--org_id", default=None)
@click.option("--name", default=None)
@click.option("--tag", default=None)
@click.option("--region", default=None)
@click.pass_context
def upload_file(ctx, **kwargs):
    output_entry(files.upload(ctx, **kwargs))


@cli.command(name="download-file")
@click.argument("file_id")
@click.option("--org_id", default=None)
@click.option("--destination", default=None)
@click.pass_context
def download_file(ctx, **kwargs):
    files.download(ctx, **kwargs)


@cli.command(name="delete-file")
@click.argument("file_ids", nargs=-1)
@click.option("--org_id", default=None)
@click.pass_context
def delete_file(ctx, file_ids, **kwargs):
    for file_id in file_ids:
        files.delete(ctx, file_id=file_id, **kwargs)


@cli.command(name="show-file")
@click.argument("file_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_file(ctx, **kwargs):
    output_entry(files.get(ctx, **kwargs))


@cli.command(name="list-config")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.pass_context
def list_config(ctx, **kwargs):
    configs = env_config.query(ctx, **kwargs)

    table = PrettyTable(
        [
            "id",
            "config_type",
            "host",
            "src_mount",
            "domain",
            "share",
            "username",
            "password",
            "dest_mount",
            "file_store_uri",
        ]
    )
    table.align = "l"
    for config in configs:
        table.add_row(
            [
                config.id,
                config.config_type,
                config.mount_hostname,
                config.mount_src_path,
                config.mount_domain,
                config.mount_share,
                config.mount_username,
                config.mount_password,
                config.mount_path,
                config.file_store_uri,
            ]
        )
    print(table)


@cli.command(name="add-config")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.option("--filename", default=None)
@click.option(
    "--config_type",
    type=click.Choice(
        [
            "configmap_mount",
            "configmap_env",
            "secret_mount",
            "secret_env",
            "mount_smb",
            "file_mount",
        ]
    ),
    prompt=True,
)
@click.option("--mount_path", default=None, prompt=True)
@click.option("--mount_src_path", default=None)
@click.option("--username", default=None)
@click.option("--hostname", default=None)
@click.option("--password", default=None)
@click.option("--share", default=None)
@click.option("--domain", default=None)
@click.option("--file_store_uri", default=None)
@click.pass_context
def add_config(ctx, **kwargs):
    output_entry(env_config.add(ctx, **kwargs).to_dict())


@cli.command(name="update-config")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.argument("id", default=None)
@click.option("--org_id", default=None)
@click.option(
    "--config_type",
    type=click.Choice(
        ["configmap_mount", "configmap_env", "secret_mount", "secret_env", "file_mount",]
    ),
)
@click.option("--mount_path", default=None)
@click.option("--mount_src_path", default=None)
@click.option("--username", default=None)
@click.option("--password", default=None)
@click.option("--share", default=None)
@click.option("--domain", default=None)
@click.option("--file_store_uri", default=None)
@click.pass_context
def update_config(ctx, **kwargs):
    output_entry(env_config.update(ctx, **kwargs).to_dict())


@cli.command(name="delete-config")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.argument("id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_config(ctx, **kwargs):
    env_config.delete(ctx, **kwargs)


@cli.command(name="list-env-vars")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.option("--org_id", default=None)
@click.option("--secret", default=True)
@click.pass_context
def list_env_vars(ctx, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    new_envs = envVar.get_env_list()

    table = PrettyTable(["key", "value"])
    table.align = "l"
    for env in new_envs:
        table.add_row([env.name, env.value])
    print(table)


@cli.command(name="add-env-var")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.argument("env_config_name", default=None)
@click.argument("env_config_value", default=None)
@click.option("--secret", default=True)
@click.pass_context
def add_env_var(ctx, env_config_name, env_config_value, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.add_env_var(env_config_name, env_config_value)


@cli.command(name="delete-env-var")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.argument("env_var_name", default=None)
@click.option("--secret", default=True)
@click.pass_context
def delete_env_var(ctx, env_var_name, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.del_env_var(env_var_name)


@cli.command(name="update-env-var")
@click.argument("application", autocompletion=app_completion)
@click.argument("env_name", autocompletion=env_completion)
@click.argument("env_config_name", default=None)
@click.argument("env_config_value", default=None)
@click.option("--secret", default=True)
@click.pass_context
def update_env_var(ctx, env_config_name, env_config_value, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.update_env_var(env_config_name, env_config_value)


@cli.command(name="get-logs")
@click.argument("org_id", default=None)
@click.option("--sub_org_id", default=None)
@click.option("--app", default=None)
@click.option("--dt_from", default=None)
@click.option("--dt_to", default=None)
@click.option("--dt_sort", default="asc")
@click.option("--limit", default=None)
@click.pass_context
def get_logs(ctx, **kwargs):
    _logs = logs.get(ctx, **kwargs)
    print(_logs)


@cli.command(name="get-top-users")
@click.argument("org_id", default=None)
@click.option("--dt_from", default=None)
@click.option("--dt_to", default=None)
@click.option("--app_id", default=None)
@click.option("--sub_org_id", default=None)
@click.option("--interval", default=None)
@click.option("--limit", default=None)
@click.pass_context
def get_top_users(ctx, **kwargs):
    _metrics = metrics.query_top(ctx, **kwargs)
    table = PrettyTable(["user_id", "email", "count"])
    table.align = "l"
    if _metrics is not None:
        for _metric in _metrics:
            table.add_row([_metric.user_id, _metric.email, _metric.count])
    print(table)


@cli.command(name="get-active-users")
@click.argument("org_id", default=None)
@click.option("--dt_from", default=None)
@click.option("--dt_to", default=None)
@click.option("--app_id", default=None)
@click.option("--sub_org_id", default=None)
@click.option("--interval", default=None)
@click.pass_context
def get_active_users(ctx, **kwargs):
    _metrics = metrics.query_active(ctx, **kwargs)
    table = PrettyTable(["time", "metric"])
    table.align = "l"
    if _metrics is not None:
        for _metric in _metrics:
            table.add_row([_metric.time, _metric.metric])
    print(table)


def _format_catalogue_entries_subtable(entries):
    table = PrettyTable(["name", "tag", "content"])
    table.align = "l"
    if entries:
        for entry in entries:
            table.add_row([entry.name, entry.tag, entry.content])
    return table


@cli.command(name="list-catalogues")
@click.option("--catalogue_category", default=None)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_catalogues(ctx, **kwargs):
    cats = catalogues.query(ctx, **kwargs)
    table = PrettyTable(["id", "category", "entries summary"])
    table.align = "l"
    for cat in cats:
        table.add_row(
            [
                cat.id,
                cat.category,
                _format_catalogue_entries_subtable(cat.catalogue_entries),
            ]
        )
    print(table)


@cli.command(name="show-catalogue")
@click.argument("catalogue_id", default=None)
@click.pass_context
def show_catalogue(ctx, **kwargs):
    output_entry(catalogues.show(ctx, **kwargs))


@cli.command(name="add-catalogue")
@click.argument("category", default=None)
@click.pass_context
def add_catalogue(ctx, **kwargs):
    output_entry(catalogues.add(ctx, **kwargs))


@cli.command(name="update-catalogue")
@click.argument("catalogue_id", default=None)
@click.option("--category", default=None)
@click.pass_context
def update_catalogue(ctx, **kwargs):
    output_entry(catalogues.update(ctx, **kwargs))


@cli.command(name="delete-catalogue")
@click.argument("catalogue_id", default=None)
@click.pass_context
def delete_catalogue(ctx, **kwargs):
    catalogues.delete(ctx, **kwargs)


@cli.command(name="list-catalogue-entries")
@click.option("--catalogue_id", default=None)
@click.option("--catalogue_category", default=None)
@click.option("--catalogue_entry_name", default=None)
@click.option("--limit", default=50, type=int)
@click.pass_context
def list_catalogue_entries(ctx, **kwargs):
    catalogue_id = kwargs.pop("catalogue_id", None)
    entries = catalogues.query_entries(ctx, catalogue_id=catalogue_id, **kwargs)
    table = PrettyTable(
        [
            "id",
            "catalogue_id",
            "category",
            "name",
            "content",
            "tag",
            "short desc",
            "long desc",
        ]
    )
    table.align = "l"
    for entry in entries:
        table.add_row(
            [
                entry.id,
                entry.catalogue_id,
                entry.catalogue_category,
                entry.name,
                entry.content,
                entry.tag,
                entry.short_description,
                entry.long_description,
            ]
        )
    print(table)


@cli.command(name="show-catalogue-entry")
@click.argument("catalogue_id", default=None)
@click.argument("entry_id", default=None)
@click.pass_context
def show_catalogue_entry(ctx, **kwargs):
    output_entry(catalogues.show_entry(ctx, **kwargs))


@cli.command(name="add-catalogue-entry")
@click.argument("catalogue_id", default=None)
@click.argument("name", default=None)
@click.option("--content", default=None)
@click.option("--tag", default=None)
@click.option("--short_description", default=None)
@click.option("--long_description", default=None)
@click.pass_context
def add_catalogue_entry(ctx, **kwargs):
    output_entry(catalogues.add_entry(ctx, **kwargs))


@cli.command(name="update-catalogue-entry")
@click.argument("catalogue_id", default=None)
@click.argument("entry_id", default=None)
@click.option("--name", default=None)
@click.option("--content", default=None)
@click.option("--tag", default=None)
@click.option("--short_description", default=None)
@click.option("--long_description", default=None)
@click.pass_context
def update_catalogue_entry(ctx, **kwargs):
    output_entry(catalogues.update_entry(ctx, **kwargs))


@cli.command(name="delete-catalogue-entry")
@click.argument("catalogue_id", default=None)
@click.argument("entry_id", default=None)
@click.pass_context
def delete_catalogue_entry(ctx, **kwargs):
    catalogues.delete_entry(ctx, **kwargs)


def _format_flat_list(items):
    return [item for item in items]


@cli.command(name="list-issuers")
@click.option("--org_id", default=None)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_issuers(ctx, **kwargs):
    _issuers = issuers.query(ctx, **kwargs)
    table = PrettyTable(
        [
            "issuer-id",
            "issuer",
            "enabled",
            "client-id",
            "client",
            "org",
            "secret",
            "application",
            "organisation_scope",
            "redirects",
            "restricted_organisations",
        ]
    )
    table.align = "l"
    for issuer in _issuers:
        if len(issuer.clients):
            for client in issuer.clients:
                table.add_row(
                    [
                        issuer.id,
                        issuer.issuer,
                        issuer.enabled,
                        client.id,
                        client.name,
                        client.org_id,
                        client.secret,
                        client.application,
                        client.organisation_scope,
                        _format_flat_list(client.redirects),
                        _format_flat_list(client.restricted_organisations),
                    ]
                )
        else:
            table.add_row(
                [
                    issuer.id,
                    issuer.issuer,
                    issuer.enabled,
                    "-",
                    "-",
                    issuer.org_id,
                    "-",
                    "-",
                    "-",
                    "-",
                    "-",
                ]
            )
    print(table)


@cli.command(name="show-issuer")
@click.argument("issuer_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_issuer(ctx, **kwargs):
    output_entry(issuers.show(ctx, **kwargs))


@cli.command(name="add-issuer")
@click.argument("issuer", default=None)
@click.argument("org_id", default=None)
@click.pass_context
def add_issuer(ctx, **kwargs):
    output_entry(issuers.add(ctx, **kwargs))


@cli.command(name="update-issuer-root")
@click.argument("issuer_id", default=None)
@click.option("--issuer", default=None)
@click.option("--org_id", default=None)
@click.option("--theme_file_id", type=str, default=None)
@click.option("--upstream_redirect_uri", default=None)
@click.option("--enabled/--disabled", default=None)
@click.pass_context
def update_issuer_root(ctx, issuer_id, **kwargs):
    output_entry(issuers.update_root(ctx, issuer_id, **kwargs))


@cli.command(name="update-issuer")
@click.argument("issuer_id", default=None)
@click.option("--theme_file_id", default=None)
@click.option("--org_id", default=None)
@click.option("--enabled/--disabled", default=None)
@click.pass_context
def update_issuer_extension(ctx, issuer_id, **kwargs):
    output_entry(issuers.update_extension(ctx, issuer_id, **kwargs))


@cli.command(name="delete-issuer")
@click.argument("issuer_id", default=None)
@click.pass_context
def delete_issuer(ctx, **kwargs):
    issuers.delete(ctx, **kwargs)


@cli.command(name="list-clients")
@click.option("--org_id", default=None)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_clients(ctx, **kwargs):
    _clients = issuers.query_clients(ctx, **kwargs)
    table = PrettyTable(
        [
            "id",
            "issuer_id",
            "org_id",
            "name",
            "secret",
            "application",
            "organisation_scope",
            "redirects",
            "restricted_organisations",
        ]
    )
    table.align = "l"
    for client in _clients:
        table.add_row(
            [
                client.id,
                client.issuer_id,
                client.org_id,
                client.name,
                client.secret,
                client.application,
                client.organisation_scope,
                _format_flat_list(client.redirects),
                _format_flat_list(client.restricted_organisations),
            ]
        )
    print(table)


@cli.command(name="show-client")
@click.argument("client_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def show_client(ctx, **kwargs):
    output_entry(issuers.show_client(ctx, **kwargs))


@cli.command(name="add-client")
@click.argument("issuer_id", default=None)
@click.argument("name", default=None)
@click.option("--secret", default=None)
@click.option("--application", default=None)
@click.option("--org_id", default=None)
@click.option(
    "--organisation_scope",
    default=None,
    type=click.Choice(["any", "here_and_down", "here_only"]),
)
@click.option("--redirect_url", default=None, multiple=True)
@click.option("--restricted_org_id", default=None, multiple=True)
@click.pass_context
def add_client(ctx, redirect_url, restricted_org_id, **kwargs):
    output_entry(
        issuers.add_client(
            ctx,
            restricted_organisations=restricted_org_id,
            redirects=redirect_url,
            **kwargs,
        )
    )


@cli.command(name="update-client")
@click.argument("client_id", default=None)
@click.option("--name", default=None)
@click.option("--secret", default=None)
@click.option("--application", default=None)
@click.option("--org_id", default=None)
@click.option("--issuer_id", default=None)
@click.option(
    "--organisation_scope",
    default=None,
    type=click.Choice(["any", "here_and_down", "here_only"]),
)
@click.pass_context
def update_client(ctx, **kwargs):
    output_entry(issuers.update_client(ctx, **kwargs,))


@cli.command(name="delete-client")
@click.argument("client_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_client(ctx, **kwargs):
    issuers.delete_client(ctx, **kwargs)


@cli.command(name="add-redirect")
@click.argument("client_id", default=None)
@click.argument("redirect_url", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def add_redirect(ctx, **kwargs):
    output_entry(issuers.add_redirect(ctx, **kwargs))


@cli.command(name="delete-redirect")
@click.argument("client_id", default=None)
@click.argument("redirect_url", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_redirect(ctx, **kwargs):
    output_entry(issuers.delete_redirect(ctx, **kwargs))


@cli.command(name="replace-redirects")
@click.argument("client_id", default=None)
@click.option("--redirect_url", default=None, multiple=True)
@click.option("--org_id", default=None)
@click.pass_context
def replace_redirets(ctx, redirect_url=None, **kwargs):
    output_entry(issuers.update_client(ctx, redirects=redirect_url, **kwargs))


@cli.command(name="add-restricted-org")
@click.argument("client_id", default=None)
@click.argument("restricted_org_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def add_restricted_org(ctx, **kwargs):
    output_entry(issuers.add_restricted_organisation(ctx, **kwargs))


@cli.command(name="delete-restricted-org")
@click.argument("client_id", default=None)
@click.argument("restricted_org_id", default=None)
@click.option("--org_id", default=None)
@click.pass_context
def delete_restricted_org(ctx, **kwargs):
    output_entry(issuers.delete_restricted_organisation(ctx, **kwargs))


@cli.command(name="replace-restricted-orgs")
@click.argument("client_id", default=None)
@click.option("--restricted_org_id", default=None, multiple=True)
@click.option("--org_id", default=None)
@click.pass_context
def replace_restricted_orgs(ctx, restricted_org_id, **kwargs):
    output_entry(
        issuers.update_client(ctx, restricted_organisations=restricted_org_id, **kwargs)
    )


@cli.command(name="list-managed-upstream-providers")
@click.argument("issuer_id", default=None)
@click.pass_context
def list_managed_upstream_providers(ctx, issuer_id=None, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("managed_upstreams", [])
    table = PrettyTable(["Name", "enabled"])
    table.align = "l"
    for upstream in upstreams:
        table.add_row([upstream["name"], upstream["enabled"]])
    print(table)


@cli.command(name="update-managed-upstream-provider")
@click.argument("issuer_id", default=None)
@click.argument("name", default=None)
@click.option("--enabled/--disabled", required=True, default=None)
@click.pass_context
def update_managed_upstream_provider(
    ctx, issuer_id=None, name=None, enabled=None, **kwargs
):
    issuer = issuers.update_managed_upstreams(ctx, issuer_id, name, enabled, **kwargs)
    if issuer:
        output_entry(issuer)


@cli.command(name="list-oidc-upstream-providers")
@click.argument("issuer_id", default=None)
@click.pass_context
def list_oidc_upstream_providers(ctx, issuer_id=None, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("oidc_upstreams", [])
    table = PrettyTable(
        [
            "name",
            "issuer",
            "client_id",
            "client_secret",
            "issuer_external_host",
            "username_key",
            "email_key",
            "email_verification_required",
            "request_user_info",
        ]
    )
    table.align = "l"
    for upstream in upstreams:
        table.add_row(
            [
                upstream["name"],
                upstream["issuer"],
                upstream["client_id"],
                upstream["client_secret"],
                upstream["issuer_external_host"],
                upstream["username_key"],
                upstream["email_key"],
                upstream["email_verification_required"],
                upstream["request_user_info"],
            ]
        )
    print(table)


@cli.command(name="update-oidc-upstream-provider")
@click.argument("issuer_id", default=None)
@click.argument("name", default=None)
@click.option("--issuer", default=None)
@click.option("--client_id", default=None)
@click.option("--client_secret", default=None)
@click.option("--issuer_external_host", default=None)
@click.option("--username_key", default=None)
@click.option("--email_key", default=None)
@click.option("--email_verification_required", type=bool, default=None)
@click.option("--request_user_info", type=bool, default=None)
@click.pass_context
def update_oidc_upstream_provider(
    ctx,
    issuer_id=None,
    name=None,
    issuer=None,
    client_id=None,
    client_secret=None,
    issuer_external_host=None,
    username_key=None,
    email_key=None,
    email_verification_required=None,
    request_user_info=None,
    **kwargs,
):
    issuer = issuers.update_oidc_upstreams(
        ctx,
        issuer_id,
        name,
        issuer,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        email_key,
        email_verification_required,
        request_user_info,
        **kwargs,
    )
    if issuer:
        output_entry(issuer)


@cli.command(name="add-oidc-upstream-provider")
@click.argument("issuer_id", default=None)
@click.argument("name", default=None)
@click.option("--issuer", default=None)
@click.option("--client_id", default=None)
@click.option("--client_secret", default=None)
@click.option("--issuer_external_host", default=None)
@click.option("--username_key", default=None)
@click.option("--email_key", default=None)
@click.option("--email_verification_required", type=bool, default=None)
@click.option("--request_user_info", type=bool, default=None)
@click.pass_context
def add_oidc_upstream_provider(
    ctx,
    issuer_id=None,
    name=None,
    issuer=None,
    client_id=None,
    client_secret=None,
    issuer_external_host=None,
    username_key=None,
    email_key=None,
    email_verification_required=None,
    request_user_info=None,
    **kwargs,
):
    issuer = issuers.add_oidc_upstreams(
        ctx,
        issuer_id,
        name,
        issuer,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        email_key,
        email_verification_required,
        request_user_info,
        **kwargs,
    )
    if issuer:
        output_entry(issuer)


@cli.command(name="delete-oidc-upstream-provider")
@click.argument("issuer_id", default=None)
@click.argument("name", default=None)
@click.pass_context
def delete_oidc_upstream_provider(ctx, issuer_id=None, name=None, **kwargs):
    issuers.delete_oidc_upstreams(ctx, issuer_id, name, **kwargs)


def _format_roles(roles):
    table = PrettyTable(["application", "roles"])
    table.align = "l"
    for k, v in roles.items():
        table.add_row([k, v])
    return table


@cli.command(name="list-elevated-permissions")
@click.option("--user_id", default=None)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_elevated_permissions(ctx, **kwargs):
    perms = permissions.query(ctx, **kwargs)
    table = PrettyTable(["user_id", "roles"])
    table.align = "l"
    for user_roles in perms:
        table.add_row(
            [user_roles.user_id, _format_roles(user_roles.roles),]
        )
    print(table)


def _show_elevated_permissions(ctx, user_id, **kwargs):
    perms = permissions.show(ctx, user_id, **kwargs)
    output_entry(perms.to_dict())


@cli.command(name="show-elevated-permissions")
@click.argument("user_id")
@click.pass_context
def show_elevated_permissions(ctx, user_id, **kwargs):
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="add-elevated-permissions")
@click.argument("user_id")
@click.argument("application")
@click.argument("name")
@click.pass_context
def add_elevated_permissions(ctx, user_id, application, name, **kwargs):
    permissions.add(ctx, user_id, application, name, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="delete-elevated-permissions")
@click.argument("user_id")
@click.argument("application")
@click.argument("name")
@click.pass_context
def delete_elevated_permissions(ctx, user_id, application, name, **kwargs):
    permissions.delete(ctx, user_id, application, name, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="clear-elevated-permissions")
@click.argument("user_id")
@click.pass_context
def clear_elevated_permissions(ctx, user_id, **kwargs):
    permissions.clear(ctx, user_id, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="create-challenge")
@click.argument("user_id")
@click.option("--challenge-type", type=click.Choice(["web_push"]), default="web_push")
@click.option("--send-now", is_flag=True)
@click.pass_context
def create_challenge(ctx, user_id, **kwargs):
    challenge = challenges.create_challenge(ctx, user_id, **kwargs)
    output_entry(challenge.to_dict())


@cli.command(name="get-challenge")
@click.argument("challenge_id")
@click.pass_context
def get_challenge(ctx, challenge_id, **kwargs):
    challenge = challenges.get_challenge(ctx, challenge_id, **kwargs)
    output_entry(challenge.to_dict())


@cli.command(name="delete-challenge")
@click.argument("challenge_id")
@click.pass_context
def delete_challenge(ctx, challenge_id, **kwargs):
    challenges.delete_challenge(ctx, challenge_id, **kwargs)


@cli.command(name="replace-challenge")
@click.argument("challenge_id")
@click.option("--send-now", is_flag=True)
@click.pass_context
def replace_challenge(ctx, challenge_id, **kwargs):
    challenge = challenges.replace_challenge(ctx, challenge_id, **kwargs)
    output_entry(challenge.to_dict())


def main():
    cli(auto_envvar_prefix="AGILICUS")


if __name__ == "__main__":
    main()
