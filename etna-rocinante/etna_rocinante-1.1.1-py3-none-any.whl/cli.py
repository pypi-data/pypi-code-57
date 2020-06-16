"""
Module managing the CLI for rocinante
"""

import argparse
from dataclasses import dataclass


@dataclass
class QueueConfigArgument:
    """
    Class representing an argument that can be passed to the program to attach a driver to a queue

    These arguments are of the form 'queue_name:driver_name:result_routing_key'
    """
    queue_name: str
    driver_name: str
    result_routing_key: str

    @staticmethod
    def parse(arg: str) -> 'QueueConfigArgument':
        try:
            return QueueConfigArgument(*arg.split(":"))
        except TypeError:
            raise ValueError


def parse_arguments():
    """
    Parse program arguments

    :return:            the parsed arguments
    """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-c", "--config-file", type=str, required=True,
        help="the path to the configuration file"
    )
    arg_parser.add_argument(
        "-r", "--root-dir", type=str, default="/var/run/rocinante",
        help="the path of the directory to use as root directory"
    )
    arg_parser.add_argument(
        "--docker-bridge-ip", type=str, default="10.9.8.7/24",
        help="the range of addresses to use for Docker's bridge interface"
    )
    arg_parser.add_argument(
        "-l", "--log-dir", type=str, default="/var/log/rocinante",
        help="the path of the directory to use as log directory"
    )
    arg_parser.add_argument(
        "--debug", action='store_true',
        help="whether debug logs should be emitted"
    )
    arg_parser.add_argument(
        "queue_config", nargs='+', type=QueueConfigArgument.parse,
        help="the queues to consume jobs from, with the driver to attach",
    )
    return arg_parser.parse_args()
