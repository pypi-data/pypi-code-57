from . import git
from . import semver
from .changelog import ChangeLog
from .version_file import VersionFile
import contextlib
import functools
import io
import myers
import safer

PREFIX = '__version__ = '
VERSION = 'VERSION'
ACTIONS = 'patch', 'minor', 'major', 'new', 'show'
__version__ = '0.9.1'


def versy(action, changelog, dry_run, message, path, verbose):
    printer = _dry_printer if dry_run else _printer

    if not dry_run:
        git.check_clean_workspace()

    vfile = VersionFile(path, printer)
    version = semver.semver(vfile.version)

    if action == 'show':
        print('Version', version, 'found in', vfile.file)
        return

    cd = verbose and not dry_run
    cl = ChangeLog(path, str(version), changelog, printer, message, cd)

    if action == 'new':
        cl.new()
        msg = 'Version v%s' % version
        git.commit([cl.file], msg, dry_run, verbose)
    else:
        new_version = str(semver.bump(version, action))
        cl.update(new_version)
        vfile.write(new_version)
        if dry_run or verbose:
            print()
        print('Version', version, '-->', new_version, 'in', vfile.file)

        if dry_run or verbose:
            print()
        msg = 'Version v%s' % new_version
        git.commit([vfile.file, cl.file], msg, dry_run, verbose)


@contextlib.contextmanager
def _dry_printer(file):
    fp = io.StringIO()

    yield functools.partial(print, file=fp)

    if file.exists():
        before = file.read_text().splitlines()
    else:
        before = []
    after = fp.getvalue().splitlines()

    print()
    print(60 * '-')
    print()
    print('%s:' % file)
    print()
    print(*myers.diff(before, after, context=2, format=True), sep='\n')


@contextlib.contextmanager
def _printer(file):
    with safer.printer(file) as _print:
        yield _print
