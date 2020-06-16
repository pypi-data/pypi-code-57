import argparse
import logging
import os
from getpass import getpass


def get_parser():
    parser = argparse.ArgumentParser(description="hashdir")

    parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "imohash"],
        default="md5",
        help="warning: imohash is a constant-time hashing library, "
        "and while being fast, it produces approximate results.",
    )

    parser.add_argument(
        "--log-level", choices=["error", "info", "debug"], default="info"
    )

    return parser


def parse_args(args):
    argument_parser = get_parser()
    args = argument_parser.parse_args(args)
    valid = validate_args(args)
    if valid:
        return args
    else:
        argument_parser.print_help()
        return None


def validate_args(args):
    return True
