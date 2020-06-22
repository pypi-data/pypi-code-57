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

from sushycli import base_system


class SystemBiosShow(base_system.BaseLister):
    """Show machine BIOS attributes"""
    def take_action(self, args):
        """System BIOS show command action

        :param args: a namespace of command-line attribute-value
            pairs that come from the user
        :returns: columns, values of data to be listed.
        """

        root = super(SystemBiosShow, self).take_action(args)

        sys_inst = root.get_system(args.system_id)

        return (['BIOS attribute', 'BIOS value'],
                [[attribute[0], attribute[1]]
                for attribute in sys_inst.bios.attributes.items()])


class SystemBiosReset(base_system.BaseCommand):
    """Reset machine BIOS attributes to default"""

    def take_action(self, args):
        """System BIOS reset command action

        :param args: a namespace of command-line attribute-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(SystemBiosReset, self).take_action(args)

        sys_inst = root.get_system(args.system_id)

        sys_inst.bios.reset_bios()

        return 0


class SystemBiosSet(base_system.BaseCommand):
    """Update the system BIOS attribute(s)

    This command allows updating BIOS attributes, On the command line,
    a declaration should typically be a number of key-value pairs.

    :Example:  foo=hello or foo="hello"

    .. note:: Attributes update is not immediate but might require
        system restart.
    """

    def get_parser(self, prog_name):
        """Set system BIOS command parser

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """
        parser = super(SystemBiosSet, self).get_parser(prog_name)

        parser.add_argument(
            'set',
            nargs='+',
            metavar="KEY=VALUE",
            action=ParseDict,
            help='Set BIOS attributes, Note that you should not '
                 'put spaces before or after the = sign.\n'
                 'If a value contains spaces, you should define '
                 'it with double quotes, for example:\n '
                 'foo="this is a sentence".')

        return parser

    def take_action(self, args):
        """Set system BIOS command action

        :param args: a namespace of command-line attribute-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(SystemBiosSet, self).take_action(args)

        sys_inst = root.get_system(args.system_id)

        sys_inst.bios.set_attributes(args.set)
        return 0


class ParseDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = {}

        if values:
            for item in values:
                split_items = item.split("=", 1)
                # we remove blanks around keys
                key = split_items[0].strip()
                value = split_items[1]

                d[key] = value

        setattr(namespace, self.dest, d)
