#!/usr/bin/env python3
import os
import sys
import traceback
import logging
import hashlib
import imohash
from . import util_logging, cli


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


def hash_file_imohash(filepath):
    return imohash.hashfile(filepath, hexdigest=True)


def hash_file_md5(filepath):
    hash_obj = hashlib.md5()
    return hash_file_hashlib(filepath, hash_obj)


def hash_file_sha1(filepath):
    hash_obj = hashlib.sha1()
    return hash_file_hashlib(filepath, hash_obj)


def hash_file_hashlib(filepath, hash_obj):
    READ_CHUNK_SIZE = 4096
    try:
        f1 = open(filepath, "rb")
    except Exception():
        f1.close()
    while 1:
        buf = f1.read(READ_CHUNK_SIZE)
        if not buf:
            break
        hash_obj.update(hashlib.md5(buf).hexdigest().encode())
    f1.close()
    return hash_obj.hexdigest()


def run(args):
    logger = util_logging.adjust_logger()

    args = cli.parse_args(args)
    if not args:
        return

    logger.setLevel(util_logging.get_log_level(args.log_level))
    if args.algorithm == "md5":
        hash_func = hash_file_md5
    if args.algorithm == "sha1":
        hash_func = hash_file_sha1
    elif args.algorithm == "imohash":
        hash_func = hash_file_imohash

    files = list(get_files(args.directory))
    result = hash_files(files, hash_func)
    print(result)


def main():
    args = sys.argv[1:]
    try:
        run(args)
    except KeyboardInterrupt:
        logging.error("Terminated on user input.")
        exit()
    except Exception:
        logging.error(
            "An unknown error have occurred." " Use '--log-level debug' to see details."
        )
        logging.debug(traceback.format_exc())
    sys.stdout.flush()


if __name__ == "__main__":
    main()
