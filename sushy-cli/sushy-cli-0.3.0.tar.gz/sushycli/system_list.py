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

from sushycli import base


class SystemList(base.BaseLister):
    """List available systems"""

    def get_parser(self, prog_name):
        """List systems command parser.

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """
        parser = super(SystemList, self).get_parser(prog_name)

        return parser

    def take_action(self, args):
        """List systems command action.

        :param args: a namespace of command-line option-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(SystemList, self).take_action(args)

        systems = root.get_system_collection()

        rows = []

        for system in systems.get_members():
            sys_inst = root.get_system(system.path)

            rows.append(
                [sys_inst.name, sys_inst.uuid, system.path]
            )

        columns = [
            'Name', 'Identity', 'System ID'
        ]

        return columns, rows
