"""Unipart OpenStack project client tools"""

from openstackclient.i18n import _
from openstackclient.identity.common import find_project
from osc_lib.command import command
from osc_lib.utils import format_list

from .network import NetworkCommand


class ProjectCommand(NetworkCommand):
    """Common base class for project commands"""

    def _create_project(self, name, description):
        """Create a project and associated default resources"""
        mgr = self.app.client_manager

        # Create project
        project = mgr.identity.projects.create(
            name=name,
            domain=None,
            description=description,
        )

        # Create network
        network = self._create_network(name, project=project)

        return {
            'project': project,
            **network,
        }

    def _delete_project(self, project):
        """Delete a project and associated default resources"""
        mgr = self.app.client_manager

        # Identify project
        if isinstance(project, str):
            # pylint: disable=broad-except
            try:
                project = find_project(mgr.identity, project)
            except Exception:
                project = None

        # Identify network
        if project is not None:
            network = next(iter(mgr.network.networks(
                name=project.name,
                project_id=project.id,
            )), None)
        else:
            network = None

        # Delete network, if applicable
        if network is not None:
            self._delete_network(network)

        # Delete project, if applicable
        if project is not None:
            mgr.identity.projects.delete(project)

        return {
            'project': project,
            'network': network,
        }


class CreateProject(ProjectCommand, command.ShowOne):
    """Create a project and associated default resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--description', metavar='<description>',
            help=_("Project description"),
        )
        parser.add_argument(
            'name', metavar='<name>',
            help=_("Project name"),
        )
        return parser

    def take_action(self, parsed_args):
        project = self._create_project(
            parsed_args.name,
            description=parsed_args.description,
        )
        return zip(*{
            'name': parsed_args.name,
            'project_id': project['project'].id,
            'network_id': project['network'].id,
            'dns_domain': project['network'].dns_domain,
            'cidr': format_list([project['subnetv6'].cidr,
                                 project['subnetv4'].cidr]),
        }.items())


class DeleteProject(ProjectCommand, command.ShowOne):
    """Delete a project and all associated resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name', metavar='<name>',
            help=_("Project name"),
        )
        return parser

    def take_action(self, parsed_args):
        project = self._delete_project(parsed_args.name)
        return zip(*{
            'name': parsed_args.name,
            'project_id': project['project'] and project['project'].id,
            'network_id': project['network'] and project['network'].id,
        }.items())
