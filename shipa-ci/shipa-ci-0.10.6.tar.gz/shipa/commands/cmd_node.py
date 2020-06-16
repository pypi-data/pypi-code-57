import sys

import click

from shipa.client.client import ShipaException
from shipa.commands import constant


@click.group()
def cli_add():
    pass


@cli_add.command("add", short_help=constant.CMD_NODE_ADD)
@click.option('-p', '--pool', help=constant.OPT_NODE_POOL, multiple=True, required=True)
@click.option('--iaas', help=constant.OPT_NODE_IAAS, default="dockermachine", show_default=True)
@click.option('--iaas-id', help=constant.OPT_NODE_IAASID)
@click.option('--address', help=constant.OPT_NODE_ADDRESS, required=True)
@click.option('--template', help=constant.OPT_NODE_TEMPLATE)
@click.option('--driver', help=constant.OPT_NODE_DRIVER, default="generic", show_default=True)
@click.option('--cacert', help=constant.OPT_NODE_CA_CERT)
@click.option('--clientcert', help=constant.OPT_NODE_CLIENT_CERT)
@click.option('--clientkey', help=constant.OPT_NODE_CLIENT_KEY)
@click.option('--register', is_flag=True, help=constant.OPT_NODE_REGISTER)
@click.pass_obj
def add(ctx, pool, iaas, iaas_id, address, template, driver, cacert, clientcert, clientkey, register):
    """Creates or registers a new node in the cluster"""

    ctx.check_valid()
    try:
        ctx.client.node_add(pools=pool, iaas=iaas, iaasid=iaas_id, address=address, template=template, driver=driver,
                            cacert=cacert, clientcert=clientcert, clientkey=clientkey, register=register)

        print('Node successfully added.')

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


@click.group()
def cli_remove():
    pass


@cli_add.command("remove", short_help=constant.CMD_NODE_REMOVE)
@click.argument("address", required=True)
@click.option('--no-rebalance', is_flag=True, help=constant.CMD_NODE_NO_REBALANCE)
@click.option('--destroy', is_flag=True, help=constant.CMD_NODE_DESTROY)
@click.pass_obj
def remove(ctx, address, no_rebalance, destroy):
    """Removes a node from the cluster"""

    ctx.check_valid()
    try:
        ctx.client.node_remove(address=address, no_rebalance=no_rebalance, destroy=destroy)

        print('Node successfully removed.')

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


cli = click.CommandCollection(sources=[cli_add, cli_remove])
