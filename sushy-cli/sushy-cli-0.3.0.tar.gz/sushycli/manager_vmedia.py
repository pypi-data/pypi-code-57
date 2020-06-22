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

from sushycli import base_vmedia


class ManagerVmediaList(base_vmedia.BaseLister):
    """Display a list of available virtual media devices identities."""

    def take_action(self, args):
        """List available virtual media devices command action"""

        root = super(ManagerVmediaList, self).take_action(args)

        mgr_inst = root.get_manager(args.manager_id)

        return (['Virtual Media ID'], [[member]
                for member in mgr_inst.virtual_media.members_identities])


class ManagerVmediaInsert(base_vmedia.BaseCommand):
    """Insert a remote media into the virtual media device.

    This command allows to insert a HTTP-based image into the virtual device.

    Note:
        All systems being managed by this manager and booting from their
        corresponding removable media device (e.g. cdrom or fd) will boot
        the image inserted into manager’s virtual media device.
    """

    def get_parser(self, prog_name):
        """Insert virtual media command parser"""

        parser = super(ManagerVmediaInsert, self).get_parser(prog_name)

        parser.add_argument(
            '--image',
            required=True,
            help='The image path for virtual media access. '
                 'The value is a HTTP based URL.')
        return parser

    def take_action(self, args):
        """Insert virtual media command action"""

        root = super(ManagerVmediaInsert, self).take_action(args)

        mgr_inst = root.get_manager(args.manager_id)

        vm_inst = mgr_inst.virtual_media.get_member(args.device_id)

        vm_inst.insert_media(args.image)

        return 0


class ManagerVmediaEject(base_vmedia.BaseCommand):
    """Detach one or all the virtual media device(s).

    Note:
        All removable media device of all systems being
        managed by this manager will be ejected.
    """

    MULTIPLE_SYSTEMS_WARNING = """"
WARNING! Multiple managed systems may be affected! If you are sure that
you want to continue this operation, please use --force argument!
"""

    def get_parser(self, prog_name):
        """Eject virtual media command parser"""

        parser = super(ManagerVmediaEject, self).get_parser(prog_name)

        parser.add_argument(
            '--force',
            nargs='?',
            const='Yes',
            help='Virtual media force eject when multiple '
                 'systems has been managed by the manager')
        return parser

    def take_action(self, args):
        """Eject virtual media command action"""

        root = super(ManagerVmediaEject, self).take_action(args)

        mgr_inst = root.get_manager(args.manager_id)

        virtmedia_col = mgr_inst.virtual_media

        vm_inst = virtmedia_col.get_member(args.device_id)

        if len(mgr_inst.systems) > 1 and not args.force:
            print(self.MULTIPLE_SYSTEMS_WARNING)
            return 0

        vm_inst.eject_media()

        return 0
