# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import argparse
import json
import os
import sys
import traceback
import urllib
from logging import error

from .datadir import get_dominant_texture_size
from .generate import generate_build_files
from .validate import validate_all_files


def handle_scan_textures(args):
    print(get_dominant_texture_size(args.directory))


def handle_validate(args):
    validate_all_files()


def handle_import(args):
    if not args.import_mods:
        return

    (mod_name, ext) = os.path.splitext(os.path.basename(args.import_mods))
    parsedurl = urllib.parse.urlparse(args.import_mods)
    print(parsedurl)
    failed = []

    with open(args.import_mods, mode="r") as file:
        if ext == ".json":
            mods = json.load(file)
            for index, mod in enumerate(mods):
                print(f"Importing mod {index}/{len(mods)}")
                try:
                    generate_build_files(
                        mod,
                        noreplace=args.noreplace,
                        allow_failures=args.allow_failures,
                        validate=args.validate,
                        repo=args.output_repo or "local",
                    )
                except Exception as e:
                    if args.debug:
                        traceback.print_exc()
                    error("{}", e)
                    failed.append(mod)
        else:
            for line in file.readlines():
                words = line.split()
                if len(words) > 0:
                    d = {"atom": words[0], "url": words[1]}
                    try:
                        generate_build_files(
                            d,
                            noreplace=args.noreplace,
                            allow_failures=args.allow_failures,
                            validate=args.validate,
                            repo=args.output_repo or "local",
                        )
                    except Exception as e:
                        if args.debug:
                            traceback.print_exc()
                        error("{}", e)
                        failed.append(d)
    if failed:
        error("The following mods failed to import:")
        print("\n".join(["{}".format(f.get("name", f["atom"])) for f in failed]))


def main():
    parser = argparse.ArgumentParser(
        description="Interface for creating partial pybuilds from a small amount of \
        information"
    )
    subparsers = parser.add_subparsers()
    imp = subparsers.add_parser("import", help="Subcommand for importing mods")
    imp.add_argument(
        "import_mods",
        metavar="FILE",
        help='automatically generates pybuilds for mods specified in the given file. \
        File can be one of the following formats: \nA plaintext file consisting of a \
        mod atom and url per line, separated by a space. \nA json file with any of the \
        fields "atom", "name", "desc"/"description", "homepage", "category", "url", \
        "file"',
    )
    imp.add_argument(
        "-n",
        "--noreplace",
        help="Skips importing mods that have already been installed",
        action="store_true",
    )
    imp.add_argument(
        "-a",
        "--allow-failures",
        help="allows importing a mod even if a nonessential part of the import \
        procedure fails, such as failing to find a dependency for a plugin.",
        action="store_true",
    )
    imp.add_argument(
        "-V",
        "--validate",
        help="Checks hashes of downloaded files if they were provided",
        action="store_true",
    )
    imp.add_argument(
        "-o",
        "--output-repo",
        help="Repository used to store the output file. If this is the same as the "
        "input repository, files may be overwritten",
    )
    imp.add_argument("--debug", help="Enables debug traces", action="store_true")

    scan = subparsers.add_parser(
        "scan_textures",
        help="Subcommand for scanning textures in data directories. "
        "Displays the dominant texture size, that is, the size of texture "
        "that takes up the most space in total.",
    )
    scan.add_argument("directory", help="Directory to (recursively) scan for textures")

    validate = subparsers.add_parser(
        "validate",
        help="Validates all nexus sources in the tree by using the API to check that "
        "a remote file matches the file we have locally",
    )

    imp.set_defaults(func=handle_import)
    scan.set_defaults(func=handle_scan_textures)
    validate.set_defaults(func=handle_validate)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    try:
        args.func(args)
    except Exception as e:
        traceback.print_exc()
        error(f"{e}")
        sys.exit(1)
