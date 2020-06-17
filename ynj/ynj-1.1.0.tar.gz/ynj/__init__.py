#!/usr/bin/env python3

import argparse as arg
import jinja2 as j2
import logging
import pprint as pp
import yaml
import sys


def setup_logger(is_debug_enabled=False):
    logger = logging.getLogger('ynj')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if(is_debug_enabled):
        logger.setLevel(logging.DEBUG)

    return logger

def main():
    parser = arg.ArgumentParser(description='Template your Jinja file using YAML variables')
    parser.add_argument('-t', '--template', nargs='?',
                        type=arg.FileType('r'), default=sys.stdin,
                        help='Jinja file - stdin by default')
    parser.add_argument('-o', '--output', nargs='?',
                        type=arg.FileType('w'), default=sys.stdout,
                        help='Output file - stdout by default')
    parser.add_argument('-f', '--values-file', nargs='?',
                        type=arg.FileType('r'), default='values.yml',
                        help='Values YAML file')
    parser.add_argument('-s', '--set', default=None,
                        help='Pass additional variables. The command line ' +
                        'variables take precedence before ones loaded from the file.')
    parser.add_argument("-I", "--include-dir", default=None,
                        help="A directory to use for searching for include directive files")
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False,
                        help='Debug mode, logs additional info to stderr')
    arguments = parser.parse_args()

    logger = setup_logger(arguments.debug)

    try:
        template = arguments.template.read()
        values = yaml.load(arguments.values_file.read(), Loader=yaml.FullLoader)
        if arguments.set is not None:
            values = { **values, **yaml.load(arguments.set, Loader=yaml.FullLoader)}

        logger.debug("Input template:\n" + template)
        logger.debug("Effective values:\n" + pp.pformat(values, indent=2))

        if arguments.include_dir:
            # We only add a search path if explicitly given (for security safety)
            jinja_env = j2.Environment(trim_blocks=True,
                                       loader=j2.FileSystemLoader(arguments.include_dir))
        else:
            jinja_env = j2.Environment(trim_blocks=True)

        output = jinja_env.from_string(template).render(values)

        arguments.output.write(output)
    except Exception as e:
        logger.error(e.__module__ + "." + e.__class__.__name__ + ":  " + str(e))
        return 1
    finally:
        arguments.values_file.close()
        arguments.template.close()
        arguments.output.close()

    return 0

