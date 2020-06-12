import sys
from pathlib import Path
import tempfile
import docker


class SASTBox(object):
    REGISTRY = 'docker.convisoappsec.com'
    TAG = 'latest'
    WORKSPACE_DIR_PATTERN = 'sastbox_workspace*'
    WORKSPACE_REPORT_PATH = ["output", "reports"]
    JSON_REPORT_PATTERN = '*.jsonreporter*.json'

    def __init__(self):
        self.docker = docker.from_env(
            version="auto"
        )

    def login(self, password, username='AWS'):
        login_args = {
            'registry': self.REGISTRY,
            'username': username,
            'password': password,
            #'reauth': True,
        }

        login_result = self.docker.login(**login_args)
        return login_result

    def run_scan_diff(self, code_dir, current_commit, previous_commit):
        self._pull()
        return self._scan_diff(
            code_dir, current_commit, previous_commit,
        )

    def _pull(self):
        self.docker.images.pull(
            self.image, tag=self.TAG
        )

    def _scan_diff(self, code_dir, current_commit, previous_commit):
        tempdir = tempfile.mkdtemp()

        environment = {
            'CURRENT_COMMIT': current_commit,
            'PREVIOUS_COMMIT': previous_commit,
        }

        volumes = {
            code_dir: {
                'bind': '/code',
                'mode': 'ro'
            },
            tempdir: {
                'bind': '/tmp',
                'mode': 'rw'
            }
        }

        command = 'main.rb -c /code --diff={PREVIOUS_COMMIT},{CURRENT_COMMIT}  -q -a'.format(
            **environment
        )


        run_args = {
            'image': self.image,
            'entrypoint': 'ruby',
            'command': command,
            #'environment': environment,
            'volumes': volumes,
            'tty': True,
            'detach': True,
        }

        container = self.docker.containers.run(**run_args)

        for line in container.logs(stream=True):
            sys.stderr.write(line)
            sys.stderr.flush()

        return self._list_reports_paths(tempdir)

    @property
    def image(self):
        return "%s/sastbox" % self.REGISTRY

    @classmethod
    def _list_reports_paths(cls, root_dir):
        sastbox_root_dir = Path(root_dir)
        sastbox_workspaces_dir = sastbox_root_dir.glob(cls.WORKSPACE_DIR_PATTERN)

        for workspace_dir in sastbox_workspaces_dir:
            sastbox_reports_dir = Path(
                workspace_dir, *cls.WORKSPACE_REPORT_PATH
            )

            for report in sastbox_reports_dir.glob(cls.JSON_REPORT_PATTERN):
                yield report
