from argparse import ArgumentParser

from .file_system_root import FilesystemRoot


class Bash:

    def __init__(self, *input):
        self._parser = ArgumentParser()
        self._parser.add_argument('--root', action='store')
        known, unknown = self._parser.parse_known_args(input)
        self.commands = unknown
        directory = known.root or FilesystemRoot.default_directory()
        self.root = FilesystemRoot(directory)
