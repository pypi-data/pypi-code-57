import wolk

PREFIX = '__version__ = '
VERSION = 'VERSION'


class VersionFile:
    def __init__(self, root, printer):
        self.printer = printer

        results = []
        for file in wolk.python(root):
            if file.name == VERSION:
                version = file.read_text().strip()
            elif file.suffix == '.py':
                version = _get_version(file)
            else:
                version = None
            if version:
                results.append((file, version))

        if not results:
            raise ValueError('No version files found')

        if len(results) > 1:
            res = ', '.join('{1} in {0}'.format(*r) for r in results)
            raise ValueError('More than one version file found: ' + res)

        self.file, self.version = results[0]

    def write(self, version):
        with self.printer(self.file) as _print:
            if self.file.name == VERSION:
                _print(version)

            else:
                for line in self.file.read_text().splitlines():
                    if line.startswith(PREFIX):
                        line = "%s'%s'" % (PREFIX, version)
                    _print(line)


def _get_version(file):
    lines = [s for s in file.read_text().splitlines() if s.startswith(PREFIX)]

    if not lines:
        return

    if len(lines) > 1:
        raise ValueError('More than one line starting "%s"' % PREFIX)

    line = lines[0]
    line = line[len(PREFIX) :]
    line = line.split('#')[0].strip()

    for quote in '"', "'":
        if len(line) > 2 and line[0] == line[-1] == quote:
            line = line[1:-1]

    return line
