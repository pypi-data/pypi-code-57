import click
from aos.usertrace.do_report import set_op, report_op
from aos.managers.addon import AddonManager
from aos.util import locale_to_unicode

@click.command("pack", short_help="Pack and make a component package",\
               help="Pack a component directory to make a package file.")
@click.argument("dir", required=True, nargs=1, type=click.Path(dir_okay=True))
def cli(dir):
    am = AddonManager()
    dir = locale_to_unicode(dir)

    set_op(op='pack', content=dir)

    am.create(dir)

    set_op(result='success')
    report_op()
