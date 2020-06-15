from devyzer.commands.utiles import run_command
from devyzer.utils.cli import print_with_color
from devyzer.commands.__init__ import Command


# git add .
class AddAllCommand(Command):
    def name(self):
        return "git_add-all"

    def run(self, args, sio, project_configuration):
        command = 'git add .'
        return run_command(command)


# git add [file]
class AddFileCommand(Command):
    def name(self):
        return "git_add-file"

    def run(self, args, sio, project_configuration):
        command = 'git add '
        if 'file' in args:
            command += args['file']
        else:
            print_with_color("I need the name of the file..", '\033[91m')
            return False

        return run_command(command)


# git branch
class ListBranchesCommand(Command):
    def name(self):
        return "git_branch"

    def run(self, args, sio, project_configuration):
        command = 'git branch'
        return run_command(command)


# git clone [url]
class CLoneCommand(Command):
    def name(self):
        return "git_clone"

    def run(self, args, sio, project_configuration):
        command = 'git clone '
        if 'url' in args:
            command += args['url']
        else:
            print_with_color("I need the url..", '\033[91m')
            return False

        return run_command(command)


# git commit -m [descriptive_message]
class CommitCommand(Command):
    def name(self):
        return "git_commit"

    def run(self, args, sio, project_configuration):
        command = 'git commit -m '
        if 'descriptive_message' in args:
            command += args['descriptive_message']
        else:
            print_with_color("I need the descriptive message..", '\033[91m')
            return False

        return run_command(command)


# git branch [branch_name]
class CreateBranchCommand(Command):
    def name(self):
        return "git_create_branch"

    def run(self, args, sio, project_configuration):
        command = 'git branch '
        if 'branch_name' in args:
            command += args['branch_name']
        else:
            print_with_color("I need the branch name..", '\033[91m')
            return False

        return run_command(command)


# git branch -d branch_name
class DeleteBranchCommand(Command):
    def name(self):
        return "git_delete-branch"

    def run(self, args, sio, project_configuration):
        command = 'git branch -d '
        if 'branch_name' in args:
            command += args['branch_name']
            return run_command(command)
        else:
            print_with_color("I need the branch name..", '\033[91m')
            return False


# git diff
class ShowFileDiffNotStagedCommand(Command):
    def name(self):
        return "git_diff-not-staged"

    def run(self, args, sio, project_configuration):
        command = 'git diff'
        return run_command(command)


# git diff --staged
class ShowFileDiffStagedAndLastCommand(Command):
    def name(self):
        return "git_diff-staged"

    def run(self, args, sio, project_configuration):
        command = 'git diff --staged'
        return run_command(command)


# git fetch [repo]
class FetchCommand(Command):
    def name(self):
        return "git_fetch"

    def run(self, args, sio, project_configuration):
        command = 'git fetch '
        if 'repo' in args:
            command += args['repo']
        else:
            print_with_color("I need the repository name..", '\033[91m')
            return False

        return run_command(command)


# git init [git_project_name]
class InitProjectCommand(Command):
    def name(self):
        return "git_init"

    def run(self, args, sio, project_configuration):
        command = 'git init'
        if 'git_project_name' in args:
            command += ' ' + args['git_project_name']
        return run_command(command)


# git merge [branch_name]
class MergeCommand(Command):
    def name(self):
        return "git_merge"

    def run(self, args, sio, project_configuration):
        command = 'git merge '
        if 'branch_name' in args:
            command += args['branch_name']
        else:
            print_with_color("I need the branch name..", '\033[91m')
            return False

        return run_command(command)


# git pull
class PullCommand(Command):
    def name(self):
        return "git_pull"

    def run(self, args, sio, project_configuration):
        command = 'git pull'
        run_command(command)


# git push branch_name --force
class PushCommand(Command):
    def name(self):
        return "git_push"

    def run(self, args, sio, project_configuration):
        command = 'git push '
        if 'branch_name' in args:
            command += args['branch_name']
        if 'with_force' in args and args['with_force'] is True:
            command += ' --force'

        return run_command(command)


# git reset [file]
class ResetFileCommand(Command):
    def name(self):
        return "git_reset-file"

    def run(self, args, sio, project_configuration):
        command = 'git reset '
        if 'file' in args:
            command += args['file']
        else:
            print_with_color("I need the name of the file..", '\033[91m')
            return False
        return run_command(command)


# git status
class GetStatusCommand(Command):
    def name(self):
        return "git_status"

    def run(self, args, sio, project_configuration):
        command = 'git status'
        return run_command(command)


# git checkout branch_name
class SwitchBranchCommand(Command):
    def name(self):
        return "git_switch-branch"

    def run(self, args, sio, project_configuration):
        command = 'git checkout '
        if 'branch_name' in args:
            command += args['branch_name']
            run_command(command)
        else:
            print_with_color("I need the branch name..", '\033[91m')
            return False
