import sys
import click
from aos.util import get_host_os, ProcessException
from serial.tools import miniterm
from aos.usertrace.do_report import set_op, report_op

# Make command
@click.command("monitor", short_help="Serial port monitor")
@click.argument("port", required=True, nargs=1)
@click.argument("baud", required=True, nargs=1)
def cli(port, baud):
    """ Open a simple serial monitor. """
    args = ['miniterm', port, baud]
    host_os = get_host_os()
    if host_os == 'Win32':
        args += ['--eol', 'CRLF']
    elif host_os == 'OSX':
        args += ['--eol', 'CR']
    else:
        args += ['--eol', 'LF']

    cmd_content = ' '.join([port, baud])
    set_op(op='monitor', content=cmd_content)

    sys.argv = args
    try:
        miniterm.main()
    except ProcessException as e:
        set_op(result='fail: ' + format(e))
        report_op()
        raise e

    set_op(result='success')
    report_op()
