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

import sushy

from sushycli import base_system


class SystemBootShow(base_system.BaseLister):
    """Show system boot information"""

    def take_action(self, args):
        """Show system boot information command action"""

        root = super(SystemBootShow, self).take_action(args)

        sys_inst = root.get_system(args.system_id)

        colunms = [
            'Boot mode',
            'Available boot modes',
            'Boot device',
            'Available boot devices'
        ]

        boot_modes = sorted(sys_inst.boot.allowed_values)
        boot_devices = sorted(
            sys_inst.get_allowed_system_boot_source_values())

        values = [[sys_inst.boot.mode, ', '.join(boot_modes),
                   sys_inst.boot.target, ', '.join(boot_devices)]]

        return colunms, values


class SystemBootSet(base_system.BaseCommand):
    """Set the system boot mode/device

    Change system boot mode and device specifying the frequency;
    either it is disabled, applied once or persistent for future reboots
    """

    def get_parser(self, prog_name):
        """Set boot device command parser"""

        parser = super(SystemBootSet, self).get_parser(prog_name)

        parser.add_argument(
            '--target',
            choices=['none', 'pxe', 'floppy', 'cd', 'usb', 'hdd'],
            type=lambda x: x.lower(),
            required=True,
            help='the target boot source')
        parser.add_argument(
            '--enabled',
            type=lambda x: x.lower(),
            choices=['disabled', 'once', 'continuous'],
            help='Next reboot only or persistent to all future reboots, '
                 'default is set to boot once')
        parser.add_argument(
            '--mode',
            choices=['bios', 'uefi'],
            type=lambda x: x.lower(),
            help='the machine boot mode')

        return parser

    def take_action(self, args):
        """Set boot device command action"""

        root = super(SystemBootSet, self).take_action(args)

        sys_inst = root.get_system(args.system_id)

        sys_inst.set_system_boot_source(
            args.target,
            enabled=args.enabled,
            mode=sushy.BOOT_SOURCE_MODE_UEFI
            if args.mode == 'uefi' else sushy.BOOT_SOURCE_MODE_BIOS)
        return 0
