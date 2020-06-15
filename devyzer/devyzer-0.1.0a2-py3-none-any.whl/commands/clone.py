import os

from git import Repo
from halo import Halo

from devyzer.commands.__init__ import Command
from devyzer.constants import DEFAULT_CONFIG_NAME
from devyzer.utils.cli import calculate_project_url_with_access_token, save_json_to_file
from devyzer.utils.command import filter_configuration_file, is_git_repo


class CloneCommand(Command):
    def name(self):
        return "clone"

    def run(self, args, sio, project_configuration):
        with Halo(text='Cloning project ...', spinner='dots') as sp:
            is_pass, msg = self.validate(project_configuration)
            if is_pass:
                is_cloned, msg = self._clone(project_configuration)
                if is_cloned is True:
                    sp.succeed(msg)
                    return True
            sp.fail(msg)

    @staticmethod
    def _clone(project_configuration):

        try:
            url = calculate_project_url_with_access_token(project_configuration['projectUrl'],
                                                          project_configuration['accessToken'])

            # Check if the current directory is a git repo
            # if is_git_repo(os.getcwd()):
            #     repo = Repo(os.getcwd())
            #     origin = repo.remotes.origin
            #     exit(1)

            project_dir = os.getcwd() + "/" + project_configuration['slug']
            if os.path.exists(project_dir) :
                repo = Repo(project_dir)
                o = repo.remotes.origin
                o.pull()
                os.chdir(project_dir)
                configuration_file_dir = project_dir + "/" + DEFAULT_CONFIG_NAME
                config = filter_configuration_file(project_configuration)
                save_json_to_file(config, configuration_file_dir)
                msg = "Project " + project_configuration["projectName"] + " is updated successfully"

            else:
                Repo.clone_from(url, project_dir)
                os.chdir(project_dir)
                configuration_file_dir = project_dir + "/" + DEFAULT_CONFIG_NAME
                config = filter_configuration_file(project_configuration)
                save_json_to_file(config, configuration_file_dir)
                msg = "Project " + project_configuration["projectName"] + " is cloned successfully"
        except Exception as e:

            return False, str(e)
        return True, msg

    @staticmethod
    def validate(project_configuration):
        project_url = project_configuration.get('projectUrl', None)
        msg = None
        if not project_url:
            msg = "project url is not found in project configuration ."
            return False, msg

        access_token = project_configuration.get('accessToken', None)
        if not access_token:
            msg = "access token is not found in project configuration ."
            return False, msg

        slug = project_configuration.get('slug', None)
        if not slug:
            msg = "slug is not found in project configuration ."
            return False, msg

        project_name = project_configuration.get('projectName', None)
        if not project_name:
            msg = "project name is not found in project configuration ."
            return False, msg

        return True, msg