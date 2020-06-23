"""
Python MCU programmer Command Line Interface utility
"""
# Python 3 compatibility for Python 2
from __future__ import print_function

# args, logging
import sys
import argparse
import logging

# utils
import textwrap

# pymcuprog main function
from . import pymcuprog_main
from .pymcuprog_main import WRITE_TO_HEX_MEMORIES
from .deviceinfo.memorynames import MemoryNames, MemoryNameAliases

# Helper functions
def _parse_literal(literal):
    """
    Literals can either be integers or float values.  Default is Integer
    """
    try:
        return int(literal, 0)
    except ValueError:
        return float(literal)

def main():
    """
    Entrypoint for installable CLI

    Configures the CLI and parses the arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
    Generic programmer of selected AVR, PIC and SAM devices

    Basic actions:
        - ping: reads the device ID or signature
        - read: read NVM
        - write: write NVM
        - erase: erase NVM
            '''),
        epilog=textwrap.dedent('''\
    Usage examples:

        Ping a device on-board a kit:
        - pymcuprog.py ping

        Ping a device using Atmel-ICE
        - pymcuprog.py -t atmelice -d atmega4809 -i updi ping

        Read the some bytes of flash:
        - pymcuprog.py read -m flash -o 0x80 -b 64

        Erase an UPDI device:
        - pymcuprog.py erase

        Erase a locked UPDI device:
        - pymcuprog.py ping --options chip_erase_by_key

        Set target supply voltage on a kit:
        - pymcuprog.py setsupplyvoltage -l 3.3
            '''))

    parser.add_argument("action",
                        help="action to perform",
                        # This makes the action argument optional only if -V/--version argument is given
                        nargs="?" if "-V" in sys.argv or "--version" in sys.argv else None,
                        default="ping",
                        # nargs='?', # this makes ping the default, and -h the only way to get usage()
                        choices=['ping', 'erase', 'read', 'write', 'getvoltage', 'getsupplyvoltage', 'reboot',
                                 'setsupplyvoltage', 'getusbvoltage', 'reset_target'])

    # Device to program
    parser.add_argument("-d", "--device",
                        type=str,
                        help="device to program")

    # Pack path
    parser.add_argument("-p", "--packpath",
                        type=str,
                        help="path to pack")

    # Tool to use
    parser.add_argument("-t", "--tool",
                        type=str,
                        help="tool to connect to")

    parser.add_argument("-s", "--serial_number",
                        type=str,
                        help="USB serial number of the unit to use")

    # Memtype
    memtype_helpstring = "memory area to access: {}".format(MemoryNameAliases.ALL)
    for memtype in MemoryNames.get_all():
        memtype_helpstring += ", '{}'".format(memtype)
    parser.add_argument("-m", "--memory",
                        type=str,
                        default=MemoryNameAliases.ALL,
                        help=memtype_helpstring)

    parser.add_argument("-o", "--offset",
                        type=lambda x: int(x, 0),
                        default="0",
                        help="memory byte offset to access")

    parser.add_argument("-b", "--bytes",
                        type=int,
                        default=0,
                        help="number of bytes to access")

    parser.add_argument("-l", "--literal",
                        type=_parse_literal,
                        nargs='+',
                        help="literal values to write")

    filename_helpstring_extra = "Note that when reading to hex file only "
    filename_helpstring_extra += ", ".join(WRITE_TO_HEX_MEMORIES)
    filename_helpstring_extra += " memories will be written to the hex file"
    parser.add_argument("-f", "--filename",
                        type=str,
                        help="file to write / read. "
                        "{}".format(filename_helpstring_extra))

    parser.add_argument("-c", "--clk",
                        type=str,
                        help="clock frequency in Hz (bps) for programming interface. "
                        "(eg: '-c 9600' or '-c 115k' or '-c 1M')")

    parser.add_argument("-u", "--uart",
                        type=str,
                        help="UART to use for UPDI")

    parser.add_argument("-i", "--interface",
                        type=str,
                        help="Interface to use")

    parser.add_argument("-v", "--verbose",
                        help="verbose output",
                        action="store_true")

    parser.add_argument("-vv", "--verbosedebug",
                        help="verbose debug output",
                        action="store_true")

    parser.add_argument("-V", "--version",
                        help="Print pymcuprog version number and exit",
                        action="store_true")

    parser.add_argument("--verify",
                        help="verify after write from file",
                        action="store_true")

    parser.add_argument("-x", "--timing",
                        help="add timing output",
                        action="store_true")

    # Special options
    parser.add_argument("--options",
                        type=str,
                        help="special features: chip_erase_by_key, hvpulse, hvautopounce, hvuserpounce,"
                        " locked_write_user_row")

    arguments = parser.parse_args()

    # Setup logging
    if arguments.verbose:
        logging_level = logging.INFO
    else:
        logging_level = logging.WARNING

        if arguments.verbosedebug:
            logging_level = logging.DEBUG

    return pymcuprog_main.pymcuprog(arguments, logging_level)

if __name__ == "__main__":
    sys.exit(main())
