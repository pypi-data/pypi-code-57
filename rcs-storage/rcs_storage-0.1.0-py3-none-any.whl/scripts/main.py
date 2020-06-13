from __future__ import unicode_literals

import argparse
import os
import textwrap
try:
    from urlparse import urljoin # py2
except ImportError:
    from urllib.parse import urljoin # py3

from prettytable import PrettyTable, ALL

from rcs_storage import client


def cmd():
    Command().execute()

def dict_to_row(data_dict):
    return ", ".join(["{}='{}'".format(k, v) for k, v in
                      flat_items(data_dict, delimit=False) if v])

def flat_items(data_dict, prefix='', delimiter='_', delimit=True):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            if delimit:
                prefix_next = prefix + key + delimiter
            else:
                prefix_next = prefix
            for subkey, subvalue in flat_items(value, prefix_next, delimiter,
                                               delimit):
                yield prefix + subkey, subvalue
        else:
            yield prefix + key, value


class Command(object):
    api_class = client.Manager
    command = None
    title = 'title'
    description = 'desc'
    help = 'Valid subcommands.'

    def __init__(self, parser=None):
        super().__init__()
        if parser is None:
            parser = argparse.ArgumentParser()
        self.parser = parser
        self._add_default_arguments()
        self.add_arguments()
        parser.set_defaults(func=self._exec_handle)
        self.subcommands = []
        subclasses = self._get_subclasses()
        if subclasses:
            kwargs = {k: getattr(self, k) for k in
                      ['title', 'description', 'help'] if getattr(self, k)}
            self.subparsers = parser.add_subparsers(**kwargs)
            for subclass in subclasses:
                subparser = self.subparsers.add_parser(subclass.command)
                self.subcommands.append(subclass(subparser))

    def _get_subclasses(self):
        """Get direct subclasses of this class.
        """
        return self.__class__.__subclasses__()

    def _get_api(self):
        host = (
            self.options.get('host', None)
            or os.environ.get('RCS_STORAGE_HOST',
                              'https://dashboard.storage.unimelb.edu.au/')
        )
        token = (self.options.get('token', None) or
                 os.environ.get('RCS_STORAGE_TOKEN'))
        if token is None:
            token_url = urljoin(host, '/tools/api-token/')
            token = input(
                "A token is required to authenticate with the Research Data "
                "Storage Registry.\n\nYou may obtain a token at this URL: %s"
                "\n\nA token may be set using the RCS_STORAGE_TOKEN "
                "environment variable, or by passing it in the --token flag "
                "e.g.\n  > export RCS_STORAGE_TOKEN=<token>\n  or\n"
                "  > rcs_storage collection list --token <token>"
                "\n\nEnter your token: " % token_url)
        return self.api_class(host, token)

    def _add_default_arguments(self):
        self.parser.add_argument(
            '-H', '--host',
            dest='host',
            help='Host.',
            default=None)
        self.parser.add_argument(
            '-t', '--token',
            dest='token',
            help='An access token.',
            default=None)

    def add_arguments(self):
        pass

    def execute(self):
        args = self.parser.parse_args()
        options = vars(args)
        pos_args = options.pop('args', ())
        args.func(*pos_args, **options)

    def _exec_handle(self, *args, **options):
        self.args = args
        self.options = options
        self.handle(*args, **options)

    def handle(self, *args, **options):
        self.parser.print_help()


class CollectionCommand(Command):
    api_class = client.CollectionManager
    command = 'collection'


class CollectionListCommand(CollectionCommand):
    command = 'list'

    def handle(self, *args, **options):
        collections = self._get_api()
        objects = collections.list()
        output = PrettyTable(hrules=ALL)
        output.field_names = ["code", "created", "name", "type", "status"]
        output.align["code"] = 'l'
        output.align["name"] = 'l'
        output.align["type"] = 'l'
        for obj in objects:
            output.add_row([textwrap.fill(str(obj[k]), width=30)
                            for k in output.field_names])
        print(output)


class CollectionShowCommand(CollectionCommand):
    command = 'show'

    def add_arguments(self):
        self.parser.add_argument(
            'code',
            help='The collection code.')

    def handle(self, *args, **options):
        collections = self._get_api()
        try:
            c = collections.get(options['code'])
        except client.DoesNotExist:
            print("Could not find a collection with the code '%s'."
                  % options['code'])
            return
        output = PrettyTable()
        output.field_names = ["Property", "Value"]
        output.align["Property"] = 'l'
        output.align["Value"] = 'l'
        for k, v in c.items():
            if k in ['contacts', 'products']:
                for i, contact in enumerate(v, start=0):
                    if i == 0:
                        key = k
                    else:
                        key = ''
                    output.add_row(
                        [key, textwrap.fill(dict_to_row(contact), width=70)])
            elif k not in ['url']:
                output.add_row([k, textwrap.fill(str(v), width=70)])
        print(output)


class IngestCommand(Command):
    api_class = client.IngestManager
    command = 'ingest'


class IngestUploadCommand(IngestCommand):
    command = 'upload'

    def add_arguments(self):
        self.parser.add_argument(
            'file',
            help='The path to the file to upload.')

    def handle(self, *args, **options):
        ingests = self._get_api()
        resp = ingests.upload_storage_report(options['file'])
        print(resp)
