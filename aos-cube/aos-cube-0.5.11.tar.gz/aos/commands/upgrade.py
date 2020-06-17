import click
from aos.util import popen, pqueryerr, simple_error, get_locale
from aos.managers.addon import AddonManager
from aos.usertrace.do_report import set_op, report_op

@click.group(short_help="Upgrade tools and components")
@click.pass_context
def cli(ctx):
    pass

@cli.command("aos-cube", short_help="Upgrade aos-cube to latest")
def upgrade_cube():
    """ Run pip upgrade process to keep aos-cube up-to-date. """
    set_op(op='upgrade', content="aos-cube")

    cmd = ["pip", "install", "--upgrade", "aos-cube"]
    try:
        ret = popen(cmd)
        if ret != 0:
            cmd.insert(3, "--no-cache-dir")
            ret, err = pqueryerr(cmd)
            if ret != 0:
                simple_error("Failed to run %s, error: %s" % (cmd, err.decode(get_locale())))
    except Exception as e:
        set_op(result='fail: ' + format(e))
        report_op()
        raise e

    set_op(result='success')
    report_op()

@cli.command("comp", short_help="Upgrade installed components to latest",\
             help="Upgrade the installed components (specified by 'COMPONENTS' "\
                  "argument) to latest. If 'COMPONENTS' argument not provided, "\
                  "all installed components will be checked or upgraded.")
@click.argument("components", required=False, nargs=-1, metavar="[COMPONENTS...]")
@click.option("-c", "--only-check", is_flag=True, \
              help="Do not update, only check for new version")
def update_components(components, only_check):
    am = AddonManager()

    args = []

    if components:
        args += components

    cmd_content = 'comp'
    if only_check:
        cmd_content += ' -c'
    if args:
        cmd_content += ' ' + ' '.join(args)

    set_op(op='upgrade', content=cmd_content)

    am.upgrade(only_check, *args)

    set_op(result='success')
    report_op()
