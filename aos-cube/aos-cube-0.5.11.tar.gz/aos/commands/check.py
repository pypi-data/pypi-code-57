import os, sys
import click

from aos.util import cd_aos_root, error, simple_error, pqueryerr, get_locale
from aos.constant import CHECK_WRAPPER, NOT_INSIDE_SDK_HINT
from aos.usertrace.do_report import set_op, report_op

# Make command
@click.command("check", short_help="Do code check",
               help="Call various check scripts, depends on what check "
                    "implemented by current release.\n\nPlease try "
                    "'aos check help' to explore more...")
@click.argument("args", required=False, nargs=-1, metavar="[ARGS...]")
def cli(args):
    """ Call various check functions implemented in OS.

        Show more ARGS with: $ aos check help
    """

    # Get aos source root directory
    ret, original_dir = cd_aos_root()
    if ret != 'success':
        error(NOT_INSIDE_SDK_HINT)

    cmd_content = ''
    if args:
        cmd_content += ' '.join(list(args))

    set_op(op='check', content=cmd_content)

    source_root = os.getcwd()
    if os.path.isdir(original_dir):
        os.chdir(original_dir)

    # Run check scripts
    check_wrapper = os.path.sep.join([source_root, CHECK_WRAPPER])
    print("check_wrapper is %s" % check_wrapper)
    if os.path.isfile(check_wrapper):
        cmd = ["python", check_wrapper] + list(args)
        ret, err = pqueryerr(cmd)
        if ret != 0:
            simple_error("Failure when executing %s, error: %s" % (cmd, err.decode(get_locale())))
    else:
        error("No check scripts found for current release!")

    set_op(result='success')
    report_op()
