import argparse
import asyncio
import sys

from . import parse_gamecontrollerdb, create_devices
from .__about__ import (
    __description__,
    __version__,
)


async def main_loop(devices):
    tasks = []
    for (gamepad, ubox360) in devices:
        tasks += gamepad.create_asyncio_tasks(ubox360.write_event,
                                              ubox360.write_abs)
    for t in tasks:
        await t


def main():
    # parse args
    arg_parser = argparse.ArgumentParser(description=__description__)
    arg_parser.add_argument("-c",
                            "--controllerdb",
                            dest="controllerdb_file",
                            default="gamecontrollerdb.txt",
                            help="use this file gamecontroller database file")
    arg_parser.add_argument("-d",
                            "--device",
                            action="append",
                            dest="devices_path",
                            help="read inputs from this/these device(s)")
    arg_parser.add_argument("-v",
                            "--version",
                            action="version",
                            version="%s %s" % (__package__, __version__))
    args = arg_parser.parse_args()

    controllerdb = parse_gamecontrollerdb(args.controllerdb_file)
    devices = create_devices(controllerdb, args.devices_path)
    asyncio.run(main_loop(devices))
    return 0


if __name__ == '__main__':
    sys.exit(main())
