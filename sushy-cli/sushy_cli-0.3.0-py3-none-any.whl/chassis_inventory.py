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

from sushycli import base_chassis
from sushycli import utils


class ChassisInventoryShow(base_chassis.BaseLister):
    """Show chassis inventory information"""

    def take_action(self, args):
        """Show chassis inventory information command action.

        :param args: a namespace of command-line option-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(ChassisInventoryShow, self).take_action(args)

        ch_inst = root.get_chassis(args.chassis_id)

        columns = [
            'Identity', 'Name', 'Description', 'Manufacturer', 'Part Number',
            'Serial Number', 'SKU', 'Asset Tag', 'OEM Vendors'
        ]

        return columns, [[utils.get_resource_column(ch_inst, column)
                          for column in columns]]
