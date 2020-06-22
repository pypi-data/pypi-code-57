# -*- coding: utf-8 -*-

# Copyright 2010-2020 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import json
import sys
from urllib.parse import urlsplit
from urllib.parse import urlunsplit

from cliff import command
from cliff import lister
import sushy
from sushy import connector
import urllib3


class BaseParserMixIn(object):
    """Common bits and pieces of all `sushycli` commands.

    Does not implement any CLI command by its own.
    """

    def add_parser_options(self, parser):

        parser.add_argument(
            '--username',
            help='Redfish BMC username')

        parser.add_argument(
            '--password',
            help='Redfish BMC user password')

        parser.add_argument(
            '--service-endpoint',
            required=True,
            help='Redfish BMC service endpoint URL (e.g. '
                 'http://localhost:8000). If location part of the URL is not '
                 'specified, it defaults to `/redfish/v1`.')

        parser.add_argument(
            '--insecure', action='store_true',
            help='Do not verify server TLS certificate')

        parser.add_argument(
            '--tls-certificates', metavar='<FILE|DIR>',
            help='Path to a CA bundle or a directory containing trusted '
                 'TLS certificates.')

        parser.add_argument(
            '--show-traffic',
            action='store_true',
            help='Show Redfish HTTP message exchange.')

        return parser

    def _to_json(self, data):
        """Turn input object into JSON when possible.

        :param data: object to jsonize
        :type data: dict or str or None
        """
        if not data:
            data = {}

        elif isinstance(data, (str, bytes)):
            try:
                data = json.loads(data)

            except json.JSONDecodeError as exc:
                self.app.LOG.error(
                    'Malformed JSON document %(doc)s: %(error)s',
                    {'doc': data, 'error': exc})
                data = {}

        else:
            data = dict(data)

        return json.dumps(data, indent=2)

    def observer(self, response):
        """Pretty print HTTP request and response details.

        :param response: HTTP response object
        :type response: requests.Response
        """
        sys.stdout.write(
            '%s %s\n%s\n%s\n' % (
                response.request.method, response.request.url,
                self._to_json(response.request.headers),
                self._to_json(response.request.body)))

        sys.stdout.write(
            '%s %s\n%s\n%s\n' % (
                response.reason, response.status_code,
                self._to_json(response.headers),
                self._to_json(response.text)))

        sys.stdout.flush()

    def take_action(self, args):
        """Common base for all command actions

        :param args: a namespace of command-line option-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        url = urlsplit(args.service_endpoint, scheme='http')

        address = []
        path = []

        for idx, component in enumerate(url):
            if idx < 2:
                address.append(component)
                path.append('')
            else:
                address.append('')
                path.append(component)

        base_url = urlunsplit(address)

        kwargs = {
            'base_url': base_url,
            'username': args.username,
            'password': args.password,
        }

        verify = args.tls_certificates or not args.insecure
        if verify is not True:
            kwargs.update(verify=verify)

        path = urlunsplit(path)
        if path:
            kwargs.update(root_prefix=path)

        if args.insecure:
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)

        conn = connector.Connector(
            base_url, verify=verify,
            response_callback=args.show_traffic and self.observer)

        kwargs.update(connector=conn)

        return sushy.Sushy(**kwargs)


class BaseCommand(BaseParserMixIn, command.Command):
    """Common base for all sushycli status commands"""

    def get_parser(self, prog_name):
        """Common base for all status command parsers.

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """

        parser = super(BaseCommand, self).get_parser(prog_name)

        # Get correctly formatted help description
        parser.formatter_class = argparse.RawDescriptionHelpFormatter

        return self.add_parser_options(parser)


class BaseLister(BaseParserMixIn, lister.Lister):
    """Common base for all sushycli listing commands"""

    def get_parser(self, prog_name):
        """Common base for all listing command parsers.

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """
        parser = super(BaseLister, self).get_parser(prog_name)

        return self.add_parser_options(parser)
