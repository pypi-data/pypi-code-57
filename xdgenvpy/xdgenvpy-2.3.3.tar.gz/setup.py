# /usr/bin/env python3

from functools import lru_cache
from glob import glob
from os import getenv
from pathlib import Path
from shutil import rmtree
from subprocess import run
from sys import executable

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

PROJECT_NAME = 'xdgenvpy'
PROJECT_VERSION = '2.3.3'


@lru_cache(maxsize=2)
def read_repo_file(filename):
    """
    Reads the specified file and returns the full contents as a single string.

    :param Path|str filename: The file to read.

    :rtype: str
    :return: The full contents of the specified file.
    """
    filename = str(Path(__file__).resolve().parent.joinpath(filename))
    with open(filename) as f:
        return f.read()


def load_requirements(filename):
    """
    Loads the :code:`requirements.tx` dependency file and returns the
    dependencies as a sequence.

    The file can contain comments that follow the pound symbol (eg. '#').
    Comments will be removed, each line is stripped of leading and trailing
    whitespace, and empty lines are deleted.  Other than these basic
    transformations, the requirements are left intact.

    :param Path|str filename: The requirements file to read.

    :rtype: tuple
    :return: A sequence of requirements.
    """
    reqs = read_repo_file(filename).splitlines()
    reqs = [str(x).strip() for x in reqs]
    reqs = [x[:x.find('#')] for x in reqs if '#' in x]
    reqs = [x for x in reqs if len(x)]
    return tuple(reqs)


def get_xdgenvpy_packages():
    """
    Finds all packages within this project and only returns the production ready
    ones.  Meaning, test packages will not be included.

    :rtype tuple
    :return: A sequence of package names that will be built into the file
            distribution.
    """
    packages = find_packages()
    packages = [p for p in packages if not p.endswith('_test')]
    return tuple(packages)


def run_external(cmd):
    """
    Runs the external commands, and returns a boolean indicating if the sub-
    process exited with a status code of '0'.

    :param list|tuple cmd: The commands to run.

    :rtype boolean
    :return: Flag indicating if the sub-process exit code is '0'.
    """
    print('Running external: ' + str(cmd))
    proc = run(cmd)
    return proc.returncode == 0


def run_setuppy(args):
    """
    Passes the specified arguments into :code:`python3 setup.py ...` and returns
    a boolean indicating if the sub-process exited with a status code of '0'.

    :param list|tuple args: The arguments to pass into :code:`python3 setup.py`.

    :rtype boolean
    :return: Flag indicating if the sub-process exit code is '0'.
    """
    cmd = [executable, 'setup.py']
    cmd.extend(args)
    return run_external(tuple(cmd))


def run_twine(args):
    """
    Passes the specified arguments into :code:`twine ...` and returns a boolean
    indicating if the sub-process exited with a status code of '0'.

    :param list|tuple args: The arguments to pass into :code:`twine`.

    :rtype boolean
    :return: Flag indicating if the sub-process exit code is '0'.
    """
    cmd = ['twine']
    cmd.extend(args)
    return run_external(tuple(cmd))


def fail(msg):
    """
    :raises RuntimeError to help make readable code by chaining function calls.
    """
    raise RuntimeError(msg)


class CleanCommand(Command):
    """
    A custom clean command that removes any intermediate build directories.

    :param str description: A short description describing the command.
    :param list user_options: Sequence of CLI options for the command.
    """

    description = 'Custom clean command that forcefully removes build, dist,' \
                  ' and other similar directories.'
    user_options = []

    def __init__(self, *args, **kwargs):
        """Initialized the custom clean command with a list of directories."""
        super(CleanCommand, self).__init__(*args, **kwargs)
        project_path = Path(__file__).resolve().parent
        self._clean_paths = {
            '.coverage',
            '.pytest_cache',
            'build',
            'coverage.xml',
            'dist',
            'man/man1/xdg-env.1.gz',
            'man/man3/xdgenvpy.3.gz',
            PROJECT_NAME + '.egg-info',
        }
        self._clean_paths = {project_path.joinpath(p)
                             for p in self._clean_paths}
        self._clean_paths = {d for d in self._clean_paths if d.exists()}

    def initialize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def run(self):
        """Removes all of the intermediate build directories."""
        for path in self._clean_paths:
            if Path(path).is_file():
                print(f'removing file {path}')
                path.unlink()
            else:
                print(f'removing directory {path}')
                rmtree(path)


class BuildManPagesCommand(Command):
    """
    A custom command that builds the custom manpages.

    To view the man-pages locally, both raw and compressed, used the
    :code:`man -l <localfile>` command.

    :param str description A short description describing the command.
    :param list user_options Sequence of CLI options for the command.
    """

    description = 'Builds the manpages.'
    user_options = []

    def __init__(self, *args, **kwargs):
        """
        Initializes the command, which includes building new source and binary
        distribution files.
        """
        super(BuildManPagesCommand, self).__init__(*args, **kwargs)

    def initialize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    @staticmethod
    def run():
        """Builds the man-pages.."""
        files = tuple(glob('./man/man[0-9]/*.[0-9]'))
        # TODO How to make this work for Windows?
        run_external(('gzip',
                      '--verbose',
                      '--keep',
                      '--best',
                      '--force',
                      *files))

    @staticmethod
    def get_data_files():
        """Finds the files required by setuptool's :code:`data_files` prop."""
        return [
            ('man/man1', glob('man/man1/*.gz')),
            ('man/man3', glob('man/man3/*.gz')),
        ]


class TwineCheckCommand(Command):
    """
    A custom command that is used to validate built distribution packages before
    publishing them to public repositories.

    :param str description A short description describing the command.
    :param list user_options Sequence of CLI options for the command.
    """

    description = 'Validates built distributions.'
    user_options = []

    def __init__(self, *args, **kwargs):
        """
        Initializes the command, which includes building new source and binary
        distribution files.
        """
        super(TwineCheckCommand, self).__init__(*args, **kwargs)
        run_setuppy(['clean', 'sdist', 'bdist_wheel'])

    def initialize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    @staticmethod
    def run():
        """Performs the validation of the source and binary distributions."""
        run_twine(['check', 'dist/*']) \
            or fail('Could not check packages in dist/*')


class PublishCommand(Command):
    """
    A custom command that is used to easily publish new source and binary
    (wheel) distributions to the public PyPi repository.

    This command takes username and password credentials as arguments.  If they
    are not set, the command defaults to the :code:`$PYPI_USERNAME` and
    :code:`$PYPI_PASSWORD` environment variables.  If neither the the CLI
    arguments nor the environment variables are set, then the command will fail
    to publish the distribution files.

    :param str description A short description describing the command.
    :param list user_options Sequence of CLI options for the command.
    """

    description = 'Publishes built distributions to PyPi'
    user_options = [
        ('username=', 'u', 'The username to the PyPi repository. '
                           'Defaults to the $PYPI_USERNAME env variable.'),
        ('password=', 'p', 'The password to the PyPi repository. '
                           'Defaults to the $PYPI_PASSWORD env variable.'),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializes the publish command, which includes building and validating
        newly built source and binary distribution files.
        """
        super(PublishCommand, self).__init__(*args, **kwargs)
        run_setuppy(['clean', 'man', 'sdist', 'bdist_wheel'])
        run_twine(['check', 'dist/*']) or fail(
            'Could not check packages in dist/*')
        self._username = None
        self._password = None
        self.username = None
        self.password = None

    def initialize_options(self):
        """Initializes the CLI arguments for this command."""
        self.username = None
        self.password = None

    def finalize_options(self):
        """Finalizes the username and password credentials."""

        self._username = self.username \
            if self.username \
            else getenv('PYPI_USERNAME', None)
        if not self._username:
            fail('Must specify username, either --username or $PYPI_USERNAME')

        self._password = self.password \
            if self.password \
            else getenv('PYPI_PASSWORD', None)
        if not self._password:
            fail('Must specify username, either --password or $PYPI_PASSWORD')

    def run(self):
        """
        Publishes the built source and binary distributions to the public PyPi
        repository.
        """
        run_twine(['upload',
                   '--verbose',
                   '--username', self._username,
                   '--password', self._password,
                   'dist/*']) \
            or fail('Cannot upload source/binary distribution.')


setup(name=PROJECT_NAME,
      version=PROJECT_VERSION,

      author='Mike Durso',
      author_email='rbprogrammer@gmail.com',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      cmdclass={
          'clean': CleanCommand,
          'man': BuildManPagesCommand,
          'publish': PublishCommand,
          'twine_check': TwineCheckCommand,
      },
      data_files=BuildManPagesCommand.get_data_files(),
      description='Another XDG Base Directory Specification utility.',
      entry_points={
          'console_scripts': [
              'xdg-env = xdgenvpy.__main__:main',
          ],
      },
      install_requires=load_requirements('requirements.txt'),
      long_description=read_repo_file('README.md'),
      long_description_content_type='text/markdown',
      packages=get_xdgenvpy_packages(),
      scripts=['bin/xdg-env-completion.bash'],
      tests_require=load_requirements('requirements-test.txt'),
      url='https://gitlab.com/deliberist/xdgenvpy',
      )
