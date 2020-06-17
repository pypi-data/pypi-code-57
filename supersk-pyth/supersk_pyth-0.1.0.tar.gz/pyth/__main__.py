#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pyth entrypoint.
"""

import os
import sys
import argparse

from pyth.helper import Helper
from pyth.utils import load_csv, sanitize_path
from pyth import version


def main(argv=None):
    """The ``pyth`` program can be used as CLI with main function entrypoint.
    """

    # init arg parser
    parser = argparse.ArgumentParser(
        prog="pyth", description="Outputs the result of a Jinja2 template.")
    # positional arguments
    parser.add_argument("template", help="The name of template.")
    parser.add_argument("csv", help="The path to csv file.")

    # optional arguments
    parser.add_argument("--version", action="version",
                        version="%%(prog)s version: %s" % version.__version__,
                        help="Print program's version number and exit.")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="The path of output file.")
    parser.add_argument("-t", "--templates-dir", metavar="DIRECTORY",
                        help="The path of directory containing templates.")
    # parse args
    args = parser.parse_args(argv)

    # get csv data
    data = None
    try:
        data = load_csv(args.csv)
    except FileNotFoundError as fnf:
        print(f"Error with csv file - {fnf}")
        print("Attempt to render template with no data.")

    helper = Helper(templates_dir=args.templates_dir)
    result = helper.render_template(args.template, context_data=data)

    if result:
        # write output
#        cwd = os.getcwd()
#        output_file = os.path.join(cwd, 'output.txt')
        if args.output:
            output_file = sanitize_path(args.output)
            # file mode
            mode = 'w' if os.path.exists(output_file) else 'a'
            with open(output_file, mode) as file:
                file.write(result)
        else:
            print(result)
        sys.exit(0)
    else:
        sys.exit("Nothing to write in file.")

if __name__ == '__main__': # pragma: no cover
    main()
