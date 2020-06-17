import click
from aos.util import popen
from aos.usertrace.do_report import set_op, report_op
from aos.managers.addon import AddonManager

@click.group(short_help="Remove the installed component or package")
@click.pass_context
def cli(ctx):
    pass

@cli.command("comp", short_help="Remove components")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-a", "--all", is_flag=True, help="Uninstall all components")
def remove_component(components, all):
    am = AddonManager()

    args = []

    if components:
        args += components

    cmd_content = 'comp'
    if all:
        cmd_content += ' -a'
    if args:
        cmd_content += ' ' + ' '.join(args)

    set_op(op='remove', content=cmd_content)

    ret = am.uninstall(False, all, *args)

    res = 'success'
    if ret != 0:
        res = 'fail'

    set_op(result=res)
    report_op()

@cli.command("pypkg", short_help="Uninstall pip package")
@click.argument("pkgs", required=True, nargs=-1, metavar="[PACKAGES...]")
@click.option("-y", "--yes", is_flag=True, help="Don't ask for confirmation of uninstall deletions.")
def remove_pypkg(pkgs, yes):
    """ Run pip process to uninstall Python packages. """
    cmd_content = "pypkg"
    cmd = ["pip", "uninstall"]

    if yes:
        cmd += ["-y"]
        cmd_content += " -y"

    for p in pkgs:
        cmd += [p]
        cmd_content += " %s" % p

    set_op(op='remove', content=cmd_content)

    try:
        ret = popen(cmd)
        if ret != 0:
            set_op(result='fail: popen return none zero.')
            report_op()
    except Exception as e:
        set_op(result='fail: ' + format(e))
        report_op()
        raise e

    set_op(result='success')
    report_op()
