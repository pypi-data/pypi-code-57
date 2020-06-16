import os
import tarfile
import tempfile
import click

from shipa.gitignore import GitIgnore


class RepositoryFolder(object):
    IGNORE_FILENAME = '.shipaignore'

    def __init__(self, directory, verbose=False):
        assert directory is not None
        assert verbose is not None

        self.directory = directory
        self.verbose = verbose

        ignore_path = os.path.join(directory, self.IGNORE_FILENAME)
        lines = None
        if os.path.isfile(ignore_path) is True:
            with open(ignore_path, 'r') as f:
                lines = f.readlines()
        self.shipa_ignore = GitIgnore(lines or [])

    def create_tarfile(self):

        os.chdir(self.directory)
        if self.verbose:
            print('Create tar archive:')

        def filter(info):
            if info.name.startswith('./.git'):
                return

            filename = info.name[2:]

            if self.shipa_ignore.match(filename):
                if self.verbose:
                    print('IGNORE: ', filename)
                return

            if self.verbose:
                print('OK', filename)
            return info

        f = tempfile.TemporaryFile(suffix='.tar.gz')
        tar = tarfile.open(fileobj=f, mode="w:gz")
        tar.add(name='.',
                recursive=True,
                filter=filter)
        tar.close()
        f.seek(0)
        return f


def parse_step_interval(step_interval):
    if step_interval.endswith('s'):
        return int(step_interval[:len(step_interval) - 1])
    elif step_interval.endswith('m'):
        return int(step_interval[:len(step_interval) - 1]) * 60
    elif step_interval.endswith('h'):
        return int(step_interval[:len(step_interval) - 1]) * 60 * 60
    elif step_interval == '':
        return 1
    else:
        return step_interval


def validate_map(ctx, param, values):
    try:
        map_data = dict()
        for value in values:
            k, v = value.split('=')
            map_data[k] = v
        return map_data
    except ValueError:
        raise click.BadParameter('need to be in format KEY=VALUE')
