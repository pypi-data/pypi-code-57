# -*- coding: utf-8 -*-

# Copyright 2020 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

import sushy

from sushycli.cmd.sushycli import main
from sushycli.tests.unit import base


@mock.patch.object(sushy, 'Sushy', autospec=True)
@mock.patch.object(sushy.connector, 'Connector', autospec=True)
class SuchyCliTestCase(base.TestCase):

    @mock.patch('sys.stdout.write', autospec=True)
    def test_show_traffic(self, mock_write, mock_connector, mock_sushy):

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me', '--show-traffic'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=mock.ANY, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

    @mock.patch('sys.stdout.write', autospec=True)
    def test_insecure(self, mock_write, mock_connector, mock_sushy):

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me', '--insecure'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=False)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly', verify=False)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_tls_certificate(self, mock_write, mock_connector, mock_sushy):

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--tls-certificate', '/dev/null'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify='/dev/null')

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly', verify='/dev/null')

    @mock.patch('sys.stdout.write', autospec=True)
    def test_service_endpoint_default(
            self, mock_write, mock_connector, mock_sushy):

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

    @mock.patch('sys.stdout.write', autospec=True)
    def test_service_endpoint_mounted(
            self, mock_write, mock_connector, mock_sushy):

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me:1234/out'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me:1234', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me:1234', connector=mock_connection,
            password='fish', username='jelly',
            root_prefix='/out')

    @mock.patch('sys.stdout.write', autospec=True)
    def test_version(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_root.redfish_version = '1.2.3'

        main(['version', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+---------+\n'
                      '| Version |'
                      '\n+---------+\n'
                      '| 1.2.3   |\n'
                      '+---------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_manager_vmedia_list(
            self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_manager = mock_root.get_manager.return_value

        mock_manager.virtual_media.\
            members_identities = (
                '/redfish/v1/Managers/58893887-8974-2487-2389-841168418919/'
                'VirtualMedia/Cd',
                '/redfish/v1/Managers/58893887-8974-2487-2389-841168418919/'
                'VirtualMedia/Floppy'
            )

        main(['manager', 'vmedia', 'list',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--manager-id', '/redfish/v1/Managers/BMC'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+-----------------------------------------'
                      '--------------------------------------+\n'
                      '| Virtual Media ID                       '
                      '                                       |\n'
                      '+-----------------------------------------'
                      '--------------------------------------+\n'
                      '| /redfish/v1/Managers/58893887-8974-2487-'
                      '2389-841168418919/VirtualMedia/Cd     |\n'
                      '| /redfish/v1/Managers/58893887-8974-2487-'
                      '2389-841168418919/VirtualMedia/Floppy |\n'
                      '+----------------------------------------'
                      '---------------------------------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    def test_manager_vmedia_insert(self, mock_connector, mock_sushy):

        main(['manager', 'vmedia', 'insert',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--manager-id', '/redfish/v1/Managers/BMC',
              '--device-id', '/redfish/v1/Managers/BMC/VirtualMedia/Cd',
              '--image', 'http://fish.me/fishiso.iso'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_manager.assert_called_once_with(
            '/redfish/v1/Managers/BMC')

        mock_manager = mock_root.get_manager.return_value

        mock_vmedia = mock_manager.virtual_media.\
            get_member('/redfish/v1/Managers/BMC/VirtualMedia/Cd')
        mock_vmedia.insert_media.\
            assert_called_once_with('http://fish.me/fishiso.iso')

    def test_manager_vmedia_eject(self, mock_connector, mock_sushy):

        main(['manager', 'vmedia', 'eject',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--manager-id', '/redfish/v1/Managers/BMC',
              '--device-id', '/redfish/v1/Managers/BMC/VirtualMedia/Cd'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_manager.assert_called_once_with(
            '/redfish/v1/Managers/BMC')

        mock_manager = mock_root.get_manager.return_value

        mock_vmedia = mock_manager.virtual_media\
            .get_member('/redfish/v1/Managers/BMC/VirtualMedia/Cd')
        mock_vmedia.eject_media.assert_called_once()

    @mock.patch('sys.stdout.write', autospec=True)
    def test_system_boot_show(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value

        mock_system.boot.mode = 'Disabled'
        mock_system.boot.allowed_values = ['Pxe', 'Cd', 'Hdd']
        mock_gasbsv = mock_system.get_allowed_system_boot_source_values
        mock_gasbsv.return_value = {'hdd', 'pxe', 'cd'}
        mock_system.boot.target = 'Hdd'

        main(['system', 'boot', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+-----------+----------------------+-------------+----'
                      '--------------------+\n| Boot mode | Available boot mo'
                      'des | Boot device | Available boot devices |\n+-------'
                      '----+----------------------+-------------+------------'
                      '------------+\n| Disabled  | Cd, Hdd, Pxe         | Hd'
                      'd         | cd, hdd, pxe           |\n+-----------+---'
                      '-------------------+-------------+--------------------'
                      '----+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_system_bios_show(self, mock_write, mock_connector, mock_sushy):
        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value
        mock_system.bios.description = None
        mock_system.bios.attributes = {'BootMode': 'Uefi',
                                       'EmbeddedSata': 'Raid',
                                       'NicBoot1': 'NetworkBoot',
                                       'ProcTurboMode': 'Enabled'}

        main(['system', 'bios', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+----------------+-------------+\n'
                      '| BIOS attribute | BIOS value  |\n'
                      '+----------------+-------------+\n'
                      '| BootMode       | Uefi        |\n'
                      '| EmbeddedSata   | Raid        |\n'
                      '| NicBoot1       | NetworkBoot |\n'
                      '| ProcTurboMode  | Enabled     |\n'
                      '+----------------+-------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    def test_system_bios_reset(self, mock_connector, mock_sushy):

        main(['system', 'bios', 'reset',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_system.assert_called_once_with(
            '/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.bios.reset_bios.assert_called_once()

    def test_system_bios_set(self, mock_connector, mock_sushy):

        main(['system', 'bios', 'set',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1',
              'BootMode=Uefi', 'EmbeddedSata=Raid',
              'NicBoot1=NetworkBoot', 'ProcTurboMode=Enabled'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_system.assert_called_once_with(
            '/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.bios.set_attributes.assert_called_once_with(
            {
                "BootMode": "Uefi",
                "EmbeddedSata": "Raid",
                "NicBoot1": "NetworkBoot",
                "ProcTurboMode": "Enabled"
            }
        )

    def test_system_bios_set_with_keys_blanks(
            self, mock_connector, mock_sushy):

        main(['system', 'bios', 'set',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1',
              'BootMode  =Uefi', '  EmbeddedSata=Raid'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_system.assert_called_once_with(
            '/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.bios.set_attributes.assert_called_once_with(
            {
                "BootMode": "Uefi",
                "EmbeddedSata": "Raid",
            }
        )

    def test_system_boot_set(self, mock_connector, mock_sushy):

        main(['system', 'boot', 'set',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1',
              '--target', 'cd',
              '--enabled', 'once',
              '--mode', 'uefi'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root = mock_sushy.return_value

        mock_root.get_system.assert_called_once_with(
            '/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.set_system_boot_source.\
            assert_called_once_with(sushy.BOOT_SOURCE_TARGET_CD,
                                    enabled=sushy.BOOT_SOURCE_ENABLED_ONCE,
                                    mode=sushy.BOOT_SOURCE_MODE_UEFI)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_chassis_inventory_show(
            self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_one_chassis = mock_root.get_chassis.return_value

        mock_one_chassis.identity = 'A'
        mock_one_chassis.name = 'B'
        mock_one_chassis.description = 'C'
        mock_one_chassis.manufacturer = 'D'
        mock_one_chassis.part_number = 'E'
        mock_one_chassis.serial_number = 'F'
        mock_one_chassis.sku = 'G'
        mock_one_chassis.asset_tag = 'H'
        mock_one_chassis.oem_vendors = ['I', 'J']

        main(['chassis', 'inventory', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--chassis-id', '/redfish/v1/Chassis/1U'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+----------+------+-------------+--------------+-----'
                      '--------+---------------+-----+-----------+----------'
                      '---+\n| Identity | Name | Description | Manufacturer '
                      '| Part Number | Serial Number | SKU | Asset Tag | OEM'
                      ' Vendors |\n+----------+------+-------------+--------'
                      '------+-------------+---------------+-----+----------'
                      '-+-------------+\n| A        | B    | C           | D'
                      '            | E           | F             | G   | H  '
                      '       | I, J        |\n+----------+------+----------'
                      '---+--------------+-------------+---------------+----'
                      '-+-----------+-------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_manager_inventory_show(
            self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_manager = mock_root.get_manager.return_value

        mock_manager.identity = 'A'
        mock_manager.name = 'B'
        mock_manager.description = 'C'
        mock_manager.manufacturer = 'D'
        mock_manager.part_number = 'E'
        mock_manager.serial_number = 'F'
        mock_manager.sku = 'G'
        mock_manager.asset_tag = 'H'
        mock_manager.oem_vendors = ['I', 'J']

        main(['manager', 'inventory', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--manager-id', '/redfish/v1/Mnagers/BMC'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [

            mock.call('+----------+------+-------------+-------------+\n| Id'
                      'entity | Name | Description | OEM Vendors |\n+-------'
                      '---+------+-------------+-------------+\n| A        |'
                      ' B    | C           | I, J        |\n+----------+----'
                      '--+-------------+-------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_system_list(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock.MagicMock()

        mock_system.identity = 'A'
        mock_system.name = 'B'
        mock_system.uuid = '38947555-7742-3448-3784-823347823834'
        mock_system.path = '/redfish/v1/Systems/437XR1138R2'

        mock_systems = mock_root.get_system_collection.return_value
        mock_systems.get_members.return_value = [mock_system]
        mock_root.get_system.return_value = mock_system

        main(['system', 'list',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+------+--------------------------------------+------'
                      '---------------------------+\n| Name | Identity      '
                      '                       | System ID                   '
                      '    |\n+------+--------------------------------------'
                      '+---------------------------------+\n| B    | 3894755'
                      '5-7742-3448-3784-823347823834 | /redfish/v1/Systems/4'
                      '37XR1138R2 |\n+------+-------------------------------'
                      '-------+---------------------------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_manager_list(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_manager = mock.MagicMock()

        mock_manager.identity = 'A'
        mock_manager.name = 'B'
        mock_manager.uuid = '38947555-7742-3448-3784-823347823834'
        mock_manager.path = '/redfish/v1/Managers/BMC'

        mock_managers = mock_root.get_manager_collection.return_value
        mock_managers.get_members.return_value = [mock_manager]
        mock_root.get_manager.return_value = mock_manager

        main(['manager', 'list',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+------+--------------------------------------+------'
                      '--------------------+\n| Name | Identity             '
                      '                | Manager ID               |\n+------'
                      '+--------------------------------------+-------------'
                      '-------------+\n| B    | 38947555-7742-3448-3784-8233'
                      '47823834 | /redfish/v1/Managers/BMC |\n+------+------'
                      '--------------------------------+--------------------'
                      '------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_chassis_list(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_one_chassis = mock.MagicMock()

        mock_one_chassis.identity = 'A'
        mock_one_chassis.name = 'B'
        mock_one_chassis.uuid = '38947555-7742-3448-3784-823347823834'
        mock_one_chassis.path = '/redfish/v1/Chassis/1U'

        mock_chassis = mock_root.get_chassis_collection.return_value
        mock_chassis.get_members.return_value = [mock_one_chassis]
        mock_root.get_chassis.return_value = mock_one_chassis

        main(['chassis', 'list',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+------+--------------------------------------+------'
                      '------------------+\n| Name | Identity               '
                      '              | Chassis ID             |\n+------+---'
                      '-----------------------------------+-----------------'
                      '-------+\n| B    | 38947555-7742-3448-3784-8233478238'
                      '34 | /redfish/v1/Chassis/1U |\n+------+--------------'
                      '------------------------+------------------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_system_inventory_show(
            self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value

        mock_system.identity = 'A'
        mock_system.name = 'B'
        mock_system.description = 'C'
        mock_system.manufacturer = 'D'
        mock_system.part_number = 'E'
        mock_system.serial_number = 'F'
        mock_system.sku = 'G'
        mock_system.asset_tag = 'H'
        mock_system.oem_vendors = ['I', 'J']

        main(['system', 'inventory', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+----------+------+-------------+--------------+-----'
                      '--------+---------------+-----+-----------+----------'
                      '---+\n| Identity | Name | Description | Manufacturer '
                      '| Part Number | Serial Number | SKU | Asset Tag | OEM'
                      ' Vendors |\n+----------+------+-------------+--------'
                      '------+-------------+---------------+-----+----------'
                      '-+-------------+\n| A        | B    | C           | D'
                      '            | E           | F             | G   | H  '
                      '       | I, J        |\n+----------+------+----------'
                      '---+--------------+-------------+---------------+----'
                      '-+-----------+-------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    @mock.patch('sys.stdout.write', autospec=True)
    def test_system_power_show(self, mock_write, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value

        mock_system.power_state = 'on'

        main(['system', 'power', 'show',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        expected_calls = [
            mock.call('+-------------+\n'
                      '| Power state |\n'
                      '+-------------+\n'
                      '| on          |\n'
                      '+-------------+'),
            mock.call('\n')
        ]

        mock_write.assert_has_calls(expected_calls)

    def test_system_power_on(self, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value

        mock_system.power_state = 'off'

        main(['system', 'power',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1',
              'on'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root.get_system.assert_called_once_with('/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.reset_system.assert_called_once_with('on')

    def test_system_power_off(self, mock_connector, mock_sushy):

        mock_root = mock_sushy.return_value

        mock_system = mock_root.get_system.return_value

        mock_system.power_state = 'on'

        main(['system', 'power',
              '--username', 'jelly', '--password', 'fish',
              '--service-endpoint', 'http://fish.me',
              '--system-id', '/redfish/v1/Systems/1',
              'Off'])

        mock_connection = mock_connector.return_value

        mock_connector.assert_called_once_with(
            'http://fish.me', response_callback=False, verify=True)

        mock_sushy.assert_called_once_with(
            'http://fish.me', connector=mock_connection,
            password='fish', username='jelly')

        mock_root.get_system.assert_called_once_with('/redfish/v1/Systems/1')

        mock_system = mock_root.get_system.return_value

        mock_system.reset_system.assert_called_once_with('force off')
