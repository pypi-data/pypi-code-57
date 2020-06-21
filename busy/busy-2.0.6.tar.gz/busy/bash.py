from argparse import ArgumentParser

from .file_system_root import FilesystemRoot


class Bash:

    def __init__(self, *input):
        self._parser = ArgumentParser()
        self._parser.add_argument('--root', action='store')
        known, unknown = self._parser.parse_known_args(input)
        self.commands = unknown
        if known.root:
            self.root = FilesystemRoot(known.root)
        else:
            self.root = FilesystemRoot()
