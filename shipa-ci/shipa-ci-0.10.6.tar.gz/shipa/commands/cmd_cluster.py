import sys
import click

from shipa.client.client import ShipaException
from shipa.commands import constant
from shipa.commands.constant import KUBERNETES_PROVISIONER
from shipa.utils import validate_map


@click.group()
def cli_add():
    pass


@cli_add.command("add", short_help=constant.CMD_CLUSTER_ADD)
@click.argument("name", required=True)
@click.option('-a', '--address', help=constant.CMD_CLUSTER_ADDRESS, multiple=True)
@click.option('-d', '--default', is_flag=True, help=constant.OPT_CLUSTER_DEFAULT)
@click.option('-p', '--pools', help=constant.OPT_CLUSTER_POOL, multiple=True)
@click.option('-t', '--teams', help=constant.OPT_CLUSTER_TEAM, multiple=True)
@click.option('--token', help=constant.CMD_CLUSTER_TOKEN)
@click.option('--ingress-service', help=constant.OPT_CLUSTER_INGRESS_SERVICE)
@click.option('--ingress-ip', help=constant.OPT_CLUSTER_INGRESS_IP)
@click.option('--ingress-port', help=constant.OPT_CLUSTER_INGRESS_PORT, type=int, default=0)
@click.option('--cacert', help=constant.OPT_NODE_CA_CERT)
@click.option('--clientcert', help=constant.OPT_NODE_CLIENT_CERT)
@click.option('--clientkey', help=constant.OPT_NODE_CLIENT_KEY)
@click.option('--provisioner', help=constant.OPT_CLUSTER_PROVISIONER, default=KUBERNETES_PROVISIONER, show_default=True)
@click.option('--custom-data', help=constant.OPT_CLUSTER_CUSTOM, callback=validate_map, multiple=True)
@click.pass_obj
def add(ctx, name, address, default, pools, teams, token, ingress_service, ingress_ip, ingress_port, cacert,
        clientcert, clientkey, provisioner, custom_data):
    """Creates a kubernetes cluster definition."""

    ctx.check_valid()
    try:

        ctx.client.cluster_add(name=name, address=address, default=default, pools=pools, teams=teams, token=token,
                               ingress_service=ingress_service, ingress_ip=ingress_ip, ingress_port=ingress_port,
                               ca_cert=cacert, client_cert=clientcert, client_key=clientkey, provisioner=provisioner,
                               custom_data=custom_data)

        print('Cluster successfully added.')

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)
    except click.BadParameter as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


@click.group()
def cli_remove():
    pass


@cli_remove.command("remove", short_help=constant.OPT_CLUSTER_REMOVE)
@click.argument("name", required=True)
@click.pass_obj
def remove(ctx, name):
    """Removes a kubernetes cluster definition."""

    ctx.check_valid()
    try:
        ctx.client.cluster_remove(name=name)
        print('Cluster {0} has been removed!'.format(name))

    except ShipaException as e:
        print('{0}'.format(str(e)))
        sys.exit(1)


cli = click.CommandCollection(sources=[cli_add, cli_remove])
