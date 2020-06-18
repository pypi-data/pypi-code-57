#!/usr/bin/env python3
import os
import sys
import traceback
import logging
import hashlib
from . import util_logging, cli
from .util_hash import hash_file_imohash, hash_file_md5, hash_file_sha1


def get_files(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            yield filepath


def hash_files(files, hash_func):
    h = hashlib.md5()
    files.sort()
    for f in files:
        file_hash = hash_func(f)
        h.update(file_hash.encode())
        print(f, " ", file_hash)
    return h.hexdigest()


def run(args):
    logger = util_logging.adjust_logger()

    args = cli.parse_args(args)
    if not args:
        return

    logger.setLevel(util_logging.get_log_level(args.log_level))
    if args.algorithm == "md5":
        hash_func = hash_file_md5
    elif args.algorithm == "sha1":
        hash_func = hash_file_sha1
    elif args.algorithm == "imohash":
        hash_func = hash_file_imohash

    files = list(get_files(args.directory))
    result = hash_files(files, hash_func)
    print(result)


def main():
    EXIT_CODE_ERROR = 127
    args = sys.argv[1:]
    exit_code = 0
    try:
        run(args)
    except KeyboardInterrupt:
        logging.error("Terminated on user input.")
        exit_code = EXIT_CODE_ERROR
    except Exception as e:
        logging.error(
            "An unknown error have occurred: %s"
            ". Use '--log-level debug' to see details.",
            e,
        )
        logging.debug(traceback.extract_stack()[0])
        exit_code = EXIT_CODE_ERROR
    sys.stdout.flush()
    exit(exit_code)


if __name__ == "__main__":
    main()
