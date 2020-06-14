import sys
from contextlib import suppress
from pathlib import Path
import tempfile
import docker


class SASTBox(object):
    REGISTRY = 'docker.convisoappsec.com'
    TAG = 'latest'
    WORKSPACE_DIR_PATTERN = 'sastbox_workspace*'
    WORKSPACE_REPORT_PATH = ["output", "reports"]
    JSON_REPORT_PATTERN = '*.jsonreporter*.json'
    SUCCESS_EXIT_CODE = 0

    def __init__(self):
        self.docker = docker.from_env(
            version="auto"
        )


    def login(self, password, username='AWS'):
        login_args = {
            'registry': self.REGISTRY,
            'username': username,
            'password': password,
        }

        login_result = self.docker.login(**login_args)
        return login_result

    def run_scan_diff(self, code_dir, current_commit, previous_commit, log=None):
        return self._scan_diff(
            code_dir, current_commit, previous_commit, log
        )

    @property
    def size(self):
        registry_data = self.docker.images.get_registry_data(
            "{image}:{tag}".format(image=self.image, tag=self.TAG)
        )

        descriptor = registry_data.attrs.get('Descriptor', {})
        return descriptor.get('size') * 1024 * 1024

    def pull(self):
        '''
        {
            'status': 'Downloading',
            'progressDetail': {'current': int, 'total': int},
            'id': 'string'
        }
        '''
        size = self.size
        layers = {}
        for line in self.docker.api.pull(self.image, tag=self.TAG, stream=True, decode=True):
            status = line.get('status', '')
            detail = line.get('progressDetail', {})


            if status == 'Downloading':
                with suppress(Exception):
                    layer_id = line.get('id')
                    layer = layers.get(layer_id, {})
                    layer.update(detail)
                    layers[layer_id] = layer

                    for layer in layers.values():
                        current = layer.get('current')
                        total = layer.get('total')

                        if (current/total) > 0.98 and not layer.get('done'):
                            yield current
                            layer.update( { 'done': True } )

        yield size


    def _scan_diff(self, code_dir, current_commit, previous_commit, log):
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
            if log:
                log(line, new_line=False)

        wait_result = container.wait()
        status_code = wait_result.get('StatusCode')

        if not status_code == self.SUCCESS_EXIT_CODE:
            raise RuntimeError(
                'SASTBox exiting with error status code'
            )

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
