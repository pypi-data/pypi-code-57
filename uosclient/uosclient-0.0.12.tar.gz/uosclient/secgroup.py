"""Unipart OpenStack security group client tools"""

from openstackclient.i18n import _
from openstackclient.identity.common import find_project
from openstack.exceptions import HttpException
from osc_lib.command import command

HTTP_CONFLICT = 409


class SecurityGroupCommand(command.Command):
    """Common base class for Unipart security group commands"""

    def _ensure_security_group_rule(self, secgroup, direction='ingress',
                                    protocol='tcp', **kwargs):
        """Ensure that security group rule exists"""
        mgr = self.app.client_manager
        if 'port_range_max' not in kwargs:
            kwargs['port_range_max'] = kwargs['port_range_min']
        try:
            mgr.network.create_security_group_rule(
                security_group_id=secgroup.id,
                project_id=secgroup.project_id,
                protocol=protocol,
                direction=direction,
                **kwargs
            )
        except HttpException as exc:
            if exc.response.status_code != HTTP_CONFLICT:
                raise

    def _ensure_security_group_rules(self, secgroup, **kwargs):
        """Ensure that security group rules exist for both IPv4 and IPv6"""
        if 'remote_group_id' not in kwargs:
            kwargs['remote_ip_prefix'] = '0.0.0.0/0'
        self._ensure_security_group_rule(secgroup, ethertype='IPv4', **kwargs)
        if 'remote_group_id' not in kwargs:
            kwargs['remote_ip_prefix'] = '::/0'
        self._ensure_security_group_rule(secgroup, ethertype='IPv6', **kwargs)

    def _ensure_default_security_groups(self, project):
        """Ensure that default security groups and rules exist"""
        mgr = self.app.client_manager

        # Update default security group to allow ICMP echo
        secgroup = next(mgr.network.security_groups(
            project_id=project.id,
            name='default',
        ))
        self._ensure_security_group_rule(
            secgroup,
            ethertype='IPv4',
            remote_ip_prefix='0.0.0.0/0',
            protocol='icmp',
            port_range_min=8,  # ICMP type
            port_range_max=None,
        )
        self._ensure_security_group_rule(
            secgroup,
            ethertype='IPv6',
            remote_ip_prefix='::/0',
            protocol='icmp',
            port_range_min=128,  # ICMP type
            port_range_max=None,
        )

        # Create or update Puppet security group
        pupgroup = next(mgr.network.security_groups(
            project_id=project.id,
            name='puppet-%s' % project.name,
        ), None) or mgr.network.create_security_group(
            project_id=project.id,
            name='puppet-%s' % project.name,
            description="Puppet Master",
        )
        self._ensure_security_group_rules(pupgroup, port_range_min=80)
        self._ensure_security_group_rules(pupgroup, port_range_min=443)
        self._ensure_security_group_rules(pupgroup, port_range_min=8088)
        self._ensure_security_group_rules(pupgroup, port_range_min=8140,
                                          remote_group_id=secgroup.id)

        return {
            'default': secgroup,
            'puppet': pupgroup,
        }


class FixSecurityGroups(SecurityGroupCommand, command.ShowOne):
    """Fix default project security groups"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'project', metavar='<project>',
            help=_("Project (name or ID)"),
        )
        return parser

    def take_action(self, parsed_args):
        mgr = self.app.client_manager
        project = find_project(mgr.identity, parsed_args.project)
        groups = self._ensure_default_security_groups(project)
        return zip(*{
            'project_id': project.id,
            'default_id': groups['default'].id,
            'puppet_id': groups['puppet'].id,
        }.items())
