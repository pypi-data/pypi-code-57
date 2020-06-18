"""Unipart OpenStack network client tools"""

import time
from openstackclient.i18n import _
from openstackclient.identity.common import find_project
from osc_lib.command import command
from osc_lib.utils import format_list

from .secgroup import SecurityGroupCommand

DEFAULT_TTL = 60


class NetworkCommand(SecurityGroupCommand):
    """Common base class for network commands"""

    def _create_network(self, name, project=None, zone=None, ttl=DEFAULT_TTL):
        """Create a network and associated default resources"""
        mgr = self.app.client_manager

        # Identify project, if applicable
        if project is None:
            project = name
        if isinstance(project, str):
            project = find_project(mgr.identity, project)

        # Ensure default security group rules exist
        self._ensure_default_security_groups(project)

        # Find or create DNS zone
        mgr.dns.session.sudo_project_id = project.id
        if zone is None:
            zone = '%s.devonly.net.' % name
        if isinstance(zone, str):
            zone = next(iter(mgr.dns.zones.list({
                'name': zone,
            })), None) or mgr.dns.zones.create(
                zone,
                'PRIMARY',
                email='sysadmins@unipart.io',
                ttl=ttl,
            )

        # Create network and subnets
        network = mgr.network.create_network(
            name=name,
            project_id=project.id,
            dns_domain=zone['name'],
        )
        subnetv6 = mgr.network.create_subnet(
            name='%s-ipv6' % name,
            project_id=project.id,
            network_id=network.id,
            ip_version=6,
            ipv6_ra_mode='dhcpv6-stateful',
            ipv6_address_mode='dhcpv6-stateful',
            use_default_subnet_pool=True,
        )
        subnetv4 = mgr.network.create_subnet(
            name='%s-ipv4' % name,
            project_id=project.id,
            network_id=network.id,
            ip_version=4,
            use_default_subnet_pool=True,
        )

        # Delay to allow DHCP port to be created
        time.sleep(2)

        # Set DHCP port name
        dhcp = next(mgr.network.ports(
            network_id=network.id,
            device_owner='network:dhcp',
        ))
        mgr.network.update_port(
            dhcp,
            name='%s-dhcp' % name,
            dns_name='%s-dhcp' % name,
            description="DHCP agent",
        )

        # Create gateway port
        gateway = mgr.network.create_port(
            name='%s-gateway' % name,
            project_id=project.id,
            network_id=network.id,
            dns_name='%s-gateway' % name,
            description="Default gateway",
            device_owner='network:router_interface',
            fixed_ips=[
                {'subnet': subnetv6.id, 'ip_address': subnetv6.gateway_ip},
                {'subnet': subnetv4.id, 'ip_address': subnetv4.gateway_ip},
            ],
            port_security_enabled=False,
        )

        # Add gateway port to router
        mgr.network.add_interface_to_router(
            mgr.network.find_router('internal-external', ignore_missing=False),
            port_id=gateway.id,
        )

        return {
            'network': network,
            'subnetv6': subnetv6,
            'subnetv4': subnetv4,
            'dhcp': dhcp,
            'gateway': gateway,
            'zone': zone,
        }

    def _delete_network(self, network, delete_zone=True):
        """Delete a network and associated default resources"""
        mgr = self.app.client_manager

        # Identify network
        if isinstance(network, str):
            network = mgr.network.find_network(network)

        # Identify gateway, if applicable
        if network is not None:
            gateway = next(mgr.network.ports(
                network_id=network.id,
                name='%s-gateway' % network.name,
            ), None)
        else:
            gateway = None

        # Identify DNS zone
        if network is not None:
            zone = next(iter(mgr.dns.zones.list({
                'name': network.dns_domain,
            })), None)
        else:
            zone = None

        # Remove gateway port from router, if applicable
        if gateway is not None:
            mgr.network.remove_interface_from_router(
                mgr.network.find_router('internal-external',
                                        ignore_missing=False),
                port_id=gateway.id,
            )

        # Delete gateway port, if applicable
        if gateway is not None:
            mgr.network.delete_port(gateway)

        # Delete zone, if applicable
        if delete_zone and zone is not None:
            mgr.dns.zones.delete(zone['id'])

        # Delete network, if applicable
        if network is not None:
            mgr.network.delete_network(network)

        return {
            'network': network,
            'gateway': gateway,
            'zone': zone,
        }


class CreateNetwork(NetworkCommand, command.ShowOne):
    """Create a network and associated default resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--project', metavar='<project>',
            help=_("Project (name or ID)"),
        )
        parser.add_argument(
            '--zone', metavar='<zone>',
            help=_("DNS zone"),
        )
        parser.add_argument(
            '--ttl', metavar='<ttl>', type=int, default=DEFAULT_TTL,
            help=_("DNS default TTL"),
        )
        parser.add_argument(
            'name', metavar='<name>',
            help=_("Network name"),
        )
        return parser

    def take_action(self, parsed_args):
        network = self._create_network(
            parsed_args.name,
            project=parsed_args.project,
            zone=parsed_args.zone,
            ttl=parsed_args.ttl,
        )
        return zip(*{
            'name': parsed_args.name,
            'network_id': network['network'].id,
            'v6_subnet_id': network['subnetv6'].id,
            'v4_subnet_id': network['subnetv4'].id,
            'dhcp_port_id': network['dhcp'].id,
            'gateway_port_id': network['gateway'].id,
            'zone_id': network['zone']['id'],
            'dns_domain': network['network'].dns_domain,
            'cidr': format_list([network['subnetv6'].cidr,
                                 network['subnetv4'].cidr]),
        }.items())


class DeleteNetwork(NetworkCommand, command.ShowOne):
    """Delete a network and associated default resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--no-delete-zone', action='store_true',
            help=_("Do not delete associated DNS zone"),
        )
        parser.add_argument(
            'name', metavar='<name>',
            help=_("Network name"),
        )
        return parser

    def take_action(self, parsed_args):
        network = self._delete_network(
            parsed_args.name,
            delete_zone=(not parsed_args.no_delete_zone)
        )
        return zip(*{
            'name': parsed_args.name,
            'network_id': network['network'] and network['network'].id,
            'gateway_port_id': network['gateway'] and network['gateway'].id,
            'zone_id': network['zone'] and network['zone']['id'],
        }.items())
