from open_clmcli.clm_common import *


@clmcli.command(name='nfunction-list')
@click.pass_context
def nfunction_list(ctx, **ids):
    """Show all network function"""
    result = ctx.obj['nc'].get("nfInstances")['response']['data']

    cols = [('ID', 'id'),
            ('Name', 'name'),
            ('uid', 'uid'),
            ('Product', 'productType'),
            ('Pool Key','poolKeyId'),
            ('license Repository','licenseRepositoryId')]
    print_object(result, cols=cols)


@clmcli.command(name='nfunction-create')
@click.argument('name', metavar='<name>', required=True)
@click.option('--uid', metavar='<uid>', required=True,
        help='Ip address of the network function')
@click.option('--product-type', metavar='<type>', default="VSR",
        help='Type of the network function')
@click.option('--product-version', metavar='<version>', default="20.0",
        help='Version of the network function')
@click.option('--license-type', default="COMMERCIAL_POOL",
        help='License type')
@click.option('--license-repository', metavar='<ID>',
        help='License repository ID')
@click.option('--username', metavar='<username>', help='Login to the network function', required=True)
@click.option('--password', metavar='<password>', help='Password to the network function', required=True)
@click.option('--connection-proto', metavar='<proto>', default='SSH')
@click.pass_context
def nfunction_create(ctx, **ids):
    """Add an enterprise to the VSD"""
    params = {}
    params['name'] = ids['name']
    params['uid'] = ids['uid']
    params['productType'] = ids['product_type']
    params['productVersion'] = ids['product_version']
    params['licenseType'] = ids['license_type']
    allocatedEntitlements = [{
        'type': 'ListOfValuesEntitlement',
        'group': 'common_platform_params',
        'key': 'VSR_system_type',
        'value': {
            'chosenKey': 'VSR_integrated_base',
            'value': 1
            }
        }]
    params['allocatedEntitlements'] = allocatedEntitlements
    params['licenseRepositoryId'] = ids['license_repository']
    connectionProps = {
            'type': ids['connection_proto'],
            'userName': ids['username'],
            'password': ids['password'],
            }
    params['connectionProps'] = connectionProps
    result = ctx.obj['nc'].post("nfInstances", params)
    print(result)


@clmcli.command(name='nfunction-show')
@click.argument('id', metavar='<id>', required=True)
@click.pass_context
def nfunction_show(ctx, **ids):
    """Show information for a given network function"""
    result = ctx.obj['nc'].get("nfInstances/%s" % ids['id'])['response']['data']
    print(result)
    print_object(result, exclude=['allocatedEntitlements'], only=ctx.obj['show_only'])


@clmcli.command(name='nfunction-deploy')
@click.argument('id', metavar='<id>', required=True)
@click.pass_context
def nfunction_deploy(ctx, **ids):
    """Deploy license to a specific network instance"""
    ctx.obj['nc'].post("nfInstances/deploy/%s" % ids['id'], params=[])
