import sys
import json
import click

from serial.tools.list_ports import comports
from aos.usertrace.do_report import set_op, report_op

# Make command
@click.command("devices", short_help="List devices on serial ports",\
               help="List devices on serial ports.\n"\
                    "\nAttention: this command is deprecated! "\
                    "Please use 'aos list devices' instead.")
def cli():
    """ List devices on serial ports """

    set_op(op='devices')

    arr = []
    for p in comports():
        j = json.dumps(p.__dict__)
        arr.append(json.loads(j))
    print(json.dumps(arr, indent = 4))

    set_op(result='success')
    report_op()

    sys.exit(0)
