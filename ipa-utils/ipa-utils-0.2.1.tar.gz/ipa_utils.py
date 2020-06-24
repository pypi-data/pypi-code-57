# -*- coding: utf-8 -*-
import os
import json
import csv
import click
import yaml
import ldap3

LDAP_MAX_ENTRIES = 10 * 10000
USER_BASE_DN_TEMPLATE = u"cn=users,cn=accounts,{base_dn}"
USER_SEARCH_TEMPLATE = u"(&(objectclass=person)(uid={username}))"
USERS_SEARCH_TEMPLATE = u"(objectclass=person)"
USER_OBJECT_CLASSES = [
    "top",
    "person",
    "organizationalPerson",
    "inetOrgPerson",
    "inetUser",
    "posixAccount",
    "krbPrincipalAux",
    "krbTicketPolicyAux",
    "ipaObject",
    "ipaSshUser",
    "ipaSshGroupOfPubKeys",
    "mepOriginEntry",
]

class IpaService(object):

    def __init__(self, host=u"127.0.0.1", port=389, base_dn=None, username=None, password=None, server_params=None, connection_params=None):
        self.host = host
        self.port = port
        self.base_dn = base_dn
        self.server_params = server_params or {}
        self.server_params.update({
            "get_info": ldap3.ALL,
        })
        self.connection_params = connection_params or {}
        if username:
            self.connection_params["user"] = username
        if password:
            self.connection_params["password"] = password
        if not base_dn:
            self.base_dn = self.auto_get_base_dn()
            if not self.base_dn:
                raise RuntimeError(u"ERROR: no BaseDN provides and fetch the BaseDN failed.")

    def auto_get_base_dn(self):
        connection = self.get_connection()
        base_dns = [x for x in connection.server.info.naming_contexts if u"dc=" in x]
        if base_dns:
            return base_dns[0]
        else:
            return None

    @property
    def user_base_dn(self):
        return USER_BASE_DN_TEMPLATE.format(base_dn=self.base_dn)

    def get_connection(self):
        server = ldap3.Server(self.host, self.port, **self.server_params)
        connection = ldap3.Connection(server, **self.connection_params)
        connection.bind()
        return connection

    def get_user_entry(self, username, connection=None):
        connection = connection or self.get_connection()
        connection.search(
            search_base=self.user_base_dn,
            search_filter=USER_SEARCH_TEMPLATE.format(username=username),
            attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
            )
        if len(connection.entries):
            return connection.entries[0]
        else:
            return None

    def get_user_detail_from_entry(self, user_entry):
        user_detail = json.loads(user_entry.entry_to_json())
        data = {
            u"dn": user_detail[u"dn"],
        }
        data.update(user_detail[u"attributes"])
        for key in data.keys():
            value = data[key]
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        return data

    def get_user_detail(self, username, connection=None):
        user_entry = self.get_user_entry(username, connection)
        if not user_entry:
            return None
        return self.get_user_detail_from_entry(user_entry)

    def get_user_entries(self, connection=None, paged_size=200):
        entries = []
        connection = connection or self.get_connection()
        extra_params = {}
        counter = 0
        while True:
            counter += 1
            if counter > LDAP_MAX_ENTRIES / paged_size:
                raise RuntimeError("IpaService.get_user_entries hit the max limit: {0}".format(LDAP_MAX_ENTRIES))
            connection.search(
                search_base=self.user_base_dn,
                search_filter=USERS_SEARCH_TEMPLATE,
                attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=paged_size,
                **extra_params
                )
            entries += connection.entries
            paged_cookie = connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            if paged_cookie:
                extra_params["paged_cookie"] = paged_cookie
            else:
                break
        return entries

    def add_user_entry(self, username, user_detail, user_object_classes=None, connection=None):
        dn = "uid={},{}".format(username, self.user_base_dn)
        user_object_classes = user_object_classes or USER_OBJECT_CLASSES
        connection = connection or self.get_connection()
        connection.add(dn, user_object_classes, user_detail)
        result = connection.result
        if result["result"] == 0:
            return True
        else:
            raise RuntimeError(str(result))

    def update_user_entry(self, username, user_changes, connection=None):
        dn = "uid={},{}".format(username, self.user_base_dn)
        connection = connection or self.get_connection()
        changes = {}
        for key, value in user_changes.items():
            if isinstance(value, (list, set, tuple)):
                values = list(value)
            else:
                values = [value]
            changes[key] = [(ldap3.MODIFY_REPLACE, values)]
        connection.modify(dn, changes)
        result = connection.result
        if result["result"] == 0:
            return True
        else:
            raise RuntimeError(str(result))

    def delete_user_entry(self, username, connection=None):
        dn = "uid={},{}".format(username, self.user_base_dn)
        connection = connection or self.get_connection()
        connection.delete(dn)
        result = connection.result
        if result["result"] == 0:
            return True
        else:
            raise RuntimeError(str(result))

@click.group()
@click.option("-h", "--host", default="127.0.0.1", help=u"Server address, default to 127.0.0.1.")
@click.option("-p", "--port", default=389, type=int, help=u"Server port, default 389.")
@click.option("-u", "--username", help=u"Usesname to binding. Different user may have different field permissions. If no username provides, bind with anonymous user.")
@click.option("-P", "--password", help=u"Password for the user.")
@click.option("-b", "--base-dn", help=u"BaseDN of the ldap server. If no BaseDN provides, try to search it automatically.")
@click.pass_context
def ipa(ctx, host, port, username, password, base_dn):
    u"""Freeipa command line utils. Use sub-command to do real work.
    """
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["port"] = port
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["base_dn"] = base_dn


@ipa.command(name="get-user-detail")
@click.option("-o", "--output-format", default="yaml", type=click.Choice(['yaml', 'json']), help=u"Output format, default to yaml.")
@click.argument("username", nargs=1, required=True)
@click.pass_context
def get_user_detail(ctx, output_format, username):
    u"""Get user entry information.
    """
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user = service.get_user_detail(username)
    if not user:
        click.echo(u"Error: username [{username}] not found.".format(username=username))
        os.sys.exit(1)
    else:
        if output_format.lower() == u"json":
            click.echo(json.dumps(user, ensure_ascii=False))
        else:
            click.echo(yaml.safe_dump(user, allow_unicode=True))


@ipa.command(name="get-users")
@click.option("-o", "--output", default="users.csv")
@click.option("-e", "--encoding", default="gb18030")
@click.pass_context
def get_users(ctx, output, encoding):
    u"""Export all users to a csv file.
    """
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user_entries = service.get_user_entries()
    if not user_entries:
        print("no user entry found...")
        os.sys.exit(1)
    users = [service.get_user_detail_from_entry(user) for user in user_entries]
    user = users[0]
    headers = list(user.keys())
    headers.sort()
    rows = []
    for user in users:
        row = []
        for field in headers:
            row.append(user.get(field, None))
        rows.append(row)
    with open(output, "w", encoding=encoding, newline="") as fobj:
        f_csv = csv.writer(fobj)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


@ipa.command(name="add-user")
@click.option("-a", "--attribute", multiple=True)
@click.argument("username", nargs=1, required=True)
@click.pass_context
def add_user(ctx, username, attribute):
    u"""Create a new user entry.
    """
    attributes = attribute
    print("USERNAME:", username)
    print("ATTRIBUTES:", attributes)
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user_detail = {}
    for attribute in attributes:
        key, value = [x.strip() for x in attribute.split("=")]
        user_detail[key] = value
    try:
        result = service.add_user_entry(username, user_detail)
        print("Add user success!")
        print("New user info:")
        user = service.get_user_detail(username)
        print(json.dumps(user, ensure_ascii=False))
    except Exception as error:
        print("Add user failed!!!")
        print("Error info:")
        print(str(error))


@ipa.command(name="update-user")
@click.option("-a", "--attribute", multiple=True)
@click.argument("username", nargs=1, required=True)
@click.pass_context
def update_user(ctx, username, attribute):
    u"""Update user attributes.
    """
    attributes = attribute
    print("USERNAME:", username)
    print("ATTRIBUTES:", attributes)
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user_changes = {}
    for attribute in attributes:
        key, value = [x.strip() for x in attribute.split("=")]
        user_changes[key] = value
    try:
        result = service.update_user_entry(username, user_changes)
        print("Update user success!")
        print("New user info:")
        user = service.get_user_detail(username)
        print(json.dumps(user, ensure_ascii=False))
    except Exception as error:
        print("Update user failed!!!")
        print("Error info:")
        print(str(error))


@ipa.command(name="delete-user")
@click.argument("username", nargs=1, required=True)
@click.pass_context
def delete_user(ctx, username):
    u"""Delete a user entry.
    """
    print("USERNAME:", username)
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    try:
        result = service.delete_user_entry(username)
        print("User {} deleted!".format(username))
    except Exception as error:
        print("Delete user failed!!!")
        print("Error info:")
        print(str(error))


if __name__ == "__main__":
    ipa()
