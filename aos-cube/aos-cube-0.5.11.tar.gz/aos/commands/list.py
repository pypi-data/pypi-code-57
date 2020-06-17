import click, json
from aos.managers.addon import AddonManager
from serial.tools.list_ports import comports
from aos.usertrace.do_report import set_op, report_op

@click.group(short_help="List components and devices")
@click.pass_context
def cli(ctx):
    pass

@cli.command("devices", short_help="List devices on serial ports")
def list_devices():
    """ List devices on serial ports """

    set_op(op='list', content="devices")

    arr = []
    for p in comports():
        j = json.dumps(p.__dict__)
        arr.append(json.loads(j))
    print(json.dumps(arr, indent = 4))

    set_op(result='success')
    report_op()

@cli.command("comp", short_help="List component information",\
             help="List the information of the components (specified "\
                  "by 'COMPONENTS' argument). If 'COMPONENTS' argument "\
                  "not provided, all components's information will be list.\n"\
                  "\nIf '-r' option provided, the information of the remote "\
                  "components are list (by default, the local ones are list).\n"\
                  "\nIf '-a' option provided, all components(including "\
                  "board/mcu/arch type), will be list (by default, "\
                  "board/mcu/arch type are hidden).")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-r", "--remote", is_flag=True, help="List remote components")
@click.option("-a", "--all", is_flag=True, help="show all versions of all components")
def list_components(components, remote, all):
    am = AddonManager()

    args = []

    if components:
        args += components

    cmd_content = 'comp'
    if remote:
        cmd_content += ' -r'
    if all:
        cmd_content += ' -a'
    if args:
        cmd_content += ' ' + ' '.join(args)

    set_op(op='list', content=cmd_content)

    # Clean cached data first
    am.list(remote, all, *args)

    set_op(result='success')
    report_op()
