from . import git
from datetime import date
from pathlib import Path

NAMES = 'CHANGELOG', 'CHANGELIST', 'CHANGES', 'changelog'
SUFFIXES = {'', '.rst', '.txt', '.md'}


class ChangeLog:
    def __init__(self, root, version, file, printer, message, verbose=False):
        self.root = Path(root)
        self.version = version
        self.printer = printer
        self.file = file
        self.message = message
        self.verbose = verbose

        if not self.file:
            files = []
            for name in NAMES:
                for f in self.root.iterdir():
                    if f.stem == name and f.suffix in SUFFIXES:
                        files.append(f)
            if len(files) > 1:
                raise ValueError('Multiple changelogs: ' + ' '.join(files))
            if files:
                self.file = files[0]

    def log(self, *args, **kwds):
        if self.verbose:
            print(*args, **kwds)

    def log_print(self, *args, **kwds):
        self._print(*args, **kwds)
        self.log(' ', *args, **kwds)

    def new(self):
        file = Path(self.file or self.root / NAMES[0])
        if file.exists():
            raise ValueError('File %s already exists' % file.absolute())

        self.log(f'Creating {file}:')
        with self.printer(file) as self._print:
            self._entry(self.version, [])
            self.log_print('* %s' % (self.message or 'First release'))

        self.file = file

    def update(self, new_version):
        if not self.file:
            msg = 'Couldn\'t find a CHANGE file in %s' % self.root
            raise FileNotFoundError(msg)

        if self.message:
            messages = [self.message]
        else:
            messages = git.get_commits(str(self.version), self.root)
            messages = messages or [f'New version {self.version}']

        printed = False
        needs_empty_line = False
        with self.printer(self.file) as self._print:
            print(f'Writing {self.file}')
            if self.verbose:
                print()
            for line in self.file.read_text().splitlines():
                if not printed and self.version in line:
                    printed = True
                    if needs_empty_line:
                        self._print()
                    self._entry(new_version, messages)
                    if messages:
                        self._print()
                self._print(line)
                needs_empty_line = bool(line.strip())

            if not printed:
                if needs_empty_line:
                    self._print()
                self._entry(new_version, messages)

    def _entry(self, version, messages):
        today = date.today().strftime('%y/%m/%d')
        title = 'v%s - %s' % (version, today)
        if self.file and self.file.suffix == '.rst':
            self.log_print(title)
            self.log_print('=' * len(title))
        else:
            self.log_print('##', title)
        self.log_print()
        for message in messages:
            self.log_print('*', message)
