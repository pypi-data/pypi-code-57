from prettytable import PrettyTable
import click
from open_clmcli.clm_client import CLMConnection


def print_object(obj, cols=[], only=None, exclude=[]):
    def _format_multiple_values(values):
        """Format list in string to be printable as prettytable"""
        row_value = ""
        if type(values) is list:
            if len(values) > 0:
                last = values.pop()
                for o in values:
                    row_value += "%s\n" % o
                row_value += last
        elif type(values) is dict:
            for key in values:
                row_value += "%s : %s\n" % (key, values[key])
        return row_value

    def _print_table(obj, exclude):
        from time import gmtime
        from time import strftime
        table = PrettyTable(["Field", "Value"])
        table.align["Field"] = "l"

        for key in obj.keys():
            print(key)
            if key not in exclude:
                if type(obj[key]) in [list, dict]:
                    table.add_row([
                        key,
                        _format_multiple_values(obj[key])
                    ])
                else:
                    if key.endswith(('Date', 'Expiry')) and \
                       not obj[key] == 'null' and obj[key]:
                        value = strftime(
                            "%Y-%m-%d %H:%M:%S UTC",
                            gmtime(float(obj[key])/1000)
                        )
                    else:
                        value = obj[key]
                    table.add_row([key, value])
        print(table)

    if cols:
        # cols= column to diplay
        title = []
        key = []
        for c in cols:
            title.append(c[0])
            key.append(c[1])
        table = PrettyTable(title)
        for c in cols:
            if len(c) == 3 and 'max_width' in c[2].keys():
                table.max_width[c[0]] = c[2]['max_width']
        for line in obj:
            table.add_row([line[x] for x in key])
        print(table)
        return

    if only:
        if only in obj:
            print(obj[only])
        else:
            print("No such key : %s" % only)
    else:
        _print_table(obj, exclude)


def print_object_v2(data, options, columns=None):
    """
    Print list (columns is not None) or
    a single object (columns is None)

    Output can be a pretty table (the default) or
    a JSON (options['is_json'] is True)

    columns is the default columns to print for list. Can
    be overide with options['columns']
    """

    if columns:
        if options['show_only']:
            if options['show_only'] not in data[0]:
                raise click.exceptions.UsageError(
                        'Key "%s" is not present in the data' \
                                % options['show_only'])
            for line in data:
                print(line[options['show_only']])
            return
        # data is a list
        # check if user forces columns
        if len(options['columns']):
            cols = []
            for col in options['columns']:
                if col not in data[0]:
                    raise click.exceptions.UsageError(
                            'Key "%s" is not present in the data' \
                                    % col)
                cols.append((col, col))
        else:
            cols = columns
        title = []
        key = []
        for c in cols:
            title.append(c[0])
            key.append(c[1])
        table = PrettyTable(title)
        for c in cols:
            if len(c) == 3 and 'max_width' in c[2].keys():
                table.max_width[c[0]] = c[2]['max_width']
        for line in data:
            table.add_row([line[x] for x in key])
        print(table)
        return


def check_id(one_and_only_one=True, **ids):
    # Remove '_id' at the end of key names
    new_ids = {}
    for k, v in ids.items():
        k = '_'.join(k.split('_')[0:-1])
        new_ids[k] = v
    ids = new_ids

    # Check one and only one id is specified
    nb_ids = 0
    for k, v in ids.items():
        if v is not None:
            nb_ids += 1
            good_k = k
    if nb_ids == 0 and one_and_only_one is False:
        return None, None
    elif nb_ids != 1:
        raise click.exceptions.UsageError(
            "You must specify one and only one id in %s" % ids.keys())
    return good_k, ids[good_k]


def netmask_to_length(netmask):
    tableSubnet = {
        '0':   0,
        '128': 1,
        '192': 2,
        '224': 3,
        '240': 4,
        '248': 5,
        '252': 6,
        '254': 7,
        '255': 8
    }
    netmask_splited = str(netmask).split('.')
    length = tableSubnet[netmask_splited[0]] + \
        tableSubnet[netmask_splited[1]] + \
        tableSubnet[netmask_splited[2]] + \
        tableSubnet[netmask_splited[3]]
    return str(length)


def length_to_netmask(length):
    octet = []
    for i in [3, 2, 1, 0]:
        octet.append(str((0xffffffff << (32 - int(length)) >> i*8) & 0xff))
    return '.'.join(octet)


def print_creds(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('export CLM_USERNAME=<username>')
    click.echo('export CLM_PASSWORD=<password>')
    click.echo('export CLM_API_VERSION=5_0')
    click.echo('export CLM_API_NSP_URL=https://<host>:<port>')
    click.echo('export CLM_API_CLM_URL=https://<host>:<port>')
    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    import pbr.version
    version_info = pbr.version.VersionInfo('open-clmcli')
    click.echo(version_info.version_string())
    ctx.exit()


def print_completion(ctx, param, value):
    from os import environ
    from click._bashcomplete import get_completion_script
    if not value or ctx.resilient_parsing:
        return

    try:
        env_shell = environ['SHELL'].lower()
    except:
        click.echo('Unable to detect shell. Missing "SHELL" env variable.')
        ctx.exit()

    shell = [el for el in ['bash', 'zsh', 'fish'] if el in env_shell]
    if not shell:
        click.echo('Shell "%s" not supported for completion.' % env_shell)
        click.echo('Supported shell: "bash", "zsh", "fish".')
        ctx.exit()

    shell = shell[0]
    click.echo('# vsd %s completion start' % shell)
    print(get_completion_script("vsd", "_VSD_COMPLETE", shell).strip())
    click.echo('# vsd %s completion end' % shell)
    ctx.exit()


@click.group()
@click.option('--creds', is_flag=True, callback=print_creds, is_eager=True,
              expose_value=False, help='Display creds example')
@click.option('--version', is_flag=True, callback=print_version, is_eager=True,
              expose_value=False, help='Display version and exit')
@click.option('--nsp-api-url', metavar='<url>', envvar='NSP_API_URL',
              required=True,
              help='NSP url http(s)://hostname:port'
              ' (Env: VSD_API_NSP_URL)')
@click.option('--clm-api-url', metavar='<url>', envvar='CLM_API_URL',
              required=True,
              help='CLM url http(s)://hostname:port'
              ' (Env: CLM_API_URL)')
@click.option('--clm-username', metavar='<username>', envvar='CLM_USERNAME',
              required=True,
              help='CLM Authentication username (Env: CLM_USERNAME)')
@click.option('--clm-password', metavar='<password>', envvar='CLM_PASSWORD',
              required=True,
              help='CLM Authentication password (Env: CLM_PASSWORD)')
@click.option('--clm-api-version', metavar='<api version>',
              envvar='CLM_API_VERSION',
              required=True,
              help='CLM Authentication organization (Env: VSD_API_VERSION)')
@click.option('--clm-disable-proxy',
              envvar='CLM_DISABLE_PROXY',
              is_flag=True,
              help='Disable proxy if defined via env http(s)_proxy'
              ' (Env: CLM_DISABLE_PROXY)')
@click.option('--clm-http-proxy',
              envvar='CLM_HTTP_PROXY', metavar='<127.0.0.1:3128>',
              help='Use this proxy to reach the clm and override env'
              ' http(s)_proxy. (Env: CLM_HTTP_PROXY)')
@click.option('--clm-https-proxy',
              envvar='CLM_HTTPS_PROXY', metavar='<127.0.0.1:3128>',
              help='Use this proxy to reach the clm and override env'
              ' https_proxy. If ommited, https proxy will be set with the'
              ' given http-proxy (Env: CLM_HTTPS_PROXY)')
@click.option('--show-only', metavar='<key>',
              help='Show only the value for a given key'
                   ' (usable for show and create command)')
@click.option('--column', metavar='<name>', multiple=True,
        help='specify the column(s) to include, can be repeated')
@click.option('--json',
              help='print output in json format. Defautl is Table',
              is_flag=True)
@click.option('--debug', is_flag=True,
              help='Active debug for request and response')
@click.option('--force-auth', is_flag=True,
              help='Do not use existing APIkey. Replay authentication')
@click.option('--completion', is_flag=True, callback=print_completion,
              is_eager=True, expose_value=False,
              help='Display script to enable completion')
@click.pass_context
def clmcli(ctx, clm_username, clm_password, nsp_api_url,
           clm_api_version, clm_api_url, show_only, clm_disable_proxy,
           clm_http_proxy, clm_https_proxy, debug, force_auth, column, json):
    """Command-line interface to the CLM APIs"""
    if clm_http_proxy and clm_https_proxy:
        proxies = {
                "http": clm_http_proxy,
                "https": clm_https_proxy}
    elif clm_http_proxy and not clm_https_proxy:
        proxies = {
                "http": clm_http_proxy,
                "https": clm_http_proxy}
    elif not clm_http_proxy and not clm_https_proxy:
        proxies = {
                "http": None,
                "https": None}
    else:
        raise click.exceptions.UsageError(
                "https proxy can be ommited when http proxy is given, but not"
                " the oposite")
    nc = CLMConnection(
            clm_username,
            clm_password,
            nsp_api_url,
            clm_api_url,
            clm_api_version,
            disable_proxy=clm_disable_proxy,
            proxy=proxies,
            debug=debug,
            force_auth=force_auth
         )
    ctx.obj['nc'] = nc
    ctx.obj['show_only'] = show_only
    ctx.obj['print_options'] = {}
    ctx.obj['print_options']['show_only'] = show_only
    ctx.obj['print_options']['columns'] = column
    ctx.obj['print_options']['is_json'] = json


@clmcli.command(name='free-api')
@click.argument('ressource', metavar='<ressource>', required=True)
@click.option('--verb',
              type=click.Choice(['PUT',
                                 'GET',
                                 'POST',
                                 'DELETE']),
              default='GET',
              help='Default : GET')
@click.option('--header', metavar='<name:value>', multiple=True,
              help='Add header to the request. Can be repeated.')
@click.option('--key-value', metavar='<key:value>', multiple=True,
              help='Specify body in key/value pair.'
                   ' Can be repeated. Incompatible with --body.')
@click.option('--body', metavar='<data json>',
              help='Specify body of the request in json format.'
                   ' Incompatible with --key-value.')
@click.pass_context
def free_api(ctx, ressource, verb, header, key_value, body):
    """build your own API call (with headers and data)"""
    import json
    if key_value and body:
        raise click.exceptions.UsageError(
            "Use body or key-value")
    params = None
    if key_value:
        params = {}
        for kv in key_value:
            key, value = kv.split(':', 1)
            params[key] = value
    if body:
        try:
            params = json.loads(body)
        except ValueError:
            raise click.exceptions.UsageError(
                "Body could not be decoded as JSON")
    h = {}
    if header:
        for kv in header:
            key, value = kv.split(':', 1)
            h[key] = value
    if verb == 'GET':
        result = ctx.obj['nc'].get(ressource, headers=h)['response']['data']
    elif verb == 'PUT':
        result = ctx.obj['nc'].put(ressource, params, headers=h)
    elif verb == 'POST':
        result = ctx.obj['nc'].post(ressource, params, headers=h)
    elif verb == 'DELETE':
        result = ctx.obj['nc'].delete(ressource)
    print(json.dumps(result, indent=4))
