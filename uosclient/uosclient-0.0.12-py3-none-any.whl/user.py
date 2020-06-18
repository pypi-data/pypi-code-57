"""Unipart OpenStack user client tools"""

from openstackclient.i18n import _
from openstackclient.identity.common import find_project, find_user
from osc_lib.command import command
from osc_lib.utils import format_list
from passlib.pwd import genword

from .project import ProjectCommand


class UserCommand(ProjectCommand):
    """Common base class for user commands"""

    def _create_user(self, name):
        """Create a user and associated default resources"""
        mgr = self.app.client_manager

        # Identify member role
        role = mgr.identity.roles.find(name='_member_')

        # Generate password
        password = genword()

        # Create project
        project = self._create_project(
            name,
            description=("Personal project for %s" % name),
        )

        # Create user
        user = mgr.identity.users.create(
            name=name,
            domain=None,
            default_project=project['project'].id,
            password=password,
        )

        # Add user as project member
        mgr.identity.roles.grant(
            role.id,
            user=user.id,
            project=project['project'].id,
        )

        return {
            'user': user,
            'password': password,
            **project,
        }

    def _delete_user(self, user):
        """Delete a user and associated default resources"""
        mgr = self.app.client_manager

        # Identify user
        if isinstance(user, str):
            # pylint: disable=broad-except
            try:
                user = find_user(mgr.identity, user)
            except Exception:
                user = None

        # Identify project
        if user is not None and hasattr(user, 'default_project_id'):
            project = find_project(mgr.identity, user.default_project_id)
        else:
            project = None

        # Delete user, if applicable
        if user is not None:
            mgr.identity.users.delete(user.id)

        # Delete project, if applicable
        if project is not None:
            self._delete_project(project)

        return {
            'user': user,
            'project': project,
        }


class CreateUser(UserCommand, command.ShowOne):
    """Create a user and associated default resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name', metavar='<name>',
            help=_("User name"),
        )
        return parser

    def take_action(self, parsed_args):
        user = self._create_user(
            parsed_args.name,
        )
        return zip(*{
            'name': parsed_args.name,
            'user_id': user['user'].id,
            'project_id': user['project'].id,
            'network_id': user['network'].id,
            'dns_domain': user['network'].dns_domain,
            'cidr': format_list([user['subnetv6'].cidr,
                                 user['subnetv4'].cidr]),
            'password': user['password'],
        }.items())


class DeleteUser(UserCommand, command.ShowOne):
    """Delete a user and all associated resources"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name', metavar='<name>',
            help=_("User name"),
        )
        return parser

    def take_action(self, parsed_args):
        user = self._delete_user(parsed_args.name)
        return zip(*{
            'name': parsed_args.name,
            'user_id': user['user'] and user['user'].id,
            'project_id': user['project'] and user['project'].id,
        }.items())
