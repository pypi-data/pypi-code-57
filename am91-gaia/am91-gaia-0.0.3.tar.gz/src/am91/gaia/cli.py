import logging
import pkg_resources
from argparse import ArgumentParser

from .manifest import BaseManifest
from .generator import Generator
from .defs import APP_NAME, TEMPLATE_GROUP

def main():
    # Parse arguments
    args = parse_args()

    # Setup logger
    logging.basicConfig(level=getattr(logging, args.log_level))

    # Execute command
    args.func(args)

def parse_args():
    parser = ArgumentParser(prog=APP_NAME)
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
        default='WARNING', 
        help='logging level to show'
    )
    subparsers = parser.add_subparsers()

    # Init parser
    parser_init = subparsers.add_parser('init', help='initialize gaia project')
    parser_init.add_argument('type', help='project type (should be a valid project generator)')
    parser_init.add_argument('name', nargs='?', help='project name')
    parser_init.set_defaults(func=init)

    # List parser
    parser_list = subparsers.add_parser('list', help='list available project templates')
    parser_list.set_defaults(func=list_templates)

    args = parser.parse_args()
    if 'func' not in vars(args):
        parser.print_help()
        exit()
    return args

def init(args):
    module = None
    for mod in pkg_resources.iter_entry_points(TEMPLATE_GROUP):
        if mod.name == args.type: 
            module = mod.load()

    if module is None:
        logging.error('Template not found')
        return

    manifest = module.Manifest()

    generator = Generator(manifest)
    generator.init(args.name)
    generator.generate(module.module_name)

def list_templates(args):
    for mod in pkg_resources.iter_entry_points(TEMPLATE_GROUP):
        print(mod.name)
