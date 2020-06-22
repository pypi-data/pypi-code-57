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


class ManagerList(base.BaseLister):
    """List available managers"""

    def get_parser(self, prog_name):
        """List managers command parser.

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """
        parser = super(ManagerList, self).get_parser(prog_name)

        return parser

    def take_action(self, args):
        """List managers command action.

        :param args: a namespace of command-line option-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(ManagerList, self).take_action(args)

        managers = root.get_manager_collection()

        rows = []

        for manager in managers.get_members():
            manager_inst = root.get_manager(manager.path)

            rows.append(
                [manager_inst.name, manager_inst.uuid, manager.path]
            )

        columns = [
            'Name', 'Identity', 'Manager ID'
        ]

        return columns, rows
