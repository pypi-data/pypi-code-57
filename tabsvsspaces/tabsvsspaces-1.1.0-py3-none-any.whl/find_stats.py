import os
from pathlib import Path

from .stats import Statistics

IGNORED_FOLDERS = [
    'venv',
    'build',
    'dist',
    'generated',
    'generated-src',
]


def find_all_files(folder: Path, verbose: bool = False):
    def gen():
        for subpath, subfolders, filenames in os.walk(str(folder)):
            subfolders[:] = [subfolder for subfolder in subfolders if
                             not (subfolder.startswith('.') or subfolder.lower() in IGNORED_FOLDERS)]
            current_path = Path(subpath)
            for file in filenames:
                file_path = current_path / file
                if not file.startswith('.'):
                    yield file_path
                    if verbose:
                        print('Scanning', file_path)
                else:
                    if verbose:
                        print('Skipping', file_path)

    return list(gen())


def find_stats_for_file(filename: Path, name: str, stats: Statistics):
    extension = filename.name.split('.')[-1]
    try:
        for line in filename.read_text().split('\n'):
            spaces = False
            tabs = False
            while len(line) > 0 and line[0] in [' ', '\t']:
                if line[0] == ' ':
                    spaces = True
                if line[0] == '\t':
                    tabs = True
                line = line[1:]
            if spaces and tabs:
                stats.add_mixed_line(extension=extension,
                                     filename=name)
            elif spaces:
                stats.add_spaces(extension=extension)
            elif tabs:
                stats.add_tabs(extension=extension)
    except (UnicodeDecodeError, OSError):
        pass


def find_stats(folder: Path, verbose: bool = False) -> Statistics:
    folder = folder.resolve()
    files = find_all_files(folder, verbose=verbose)
    stats = Statistics()
    for file in files:
        find_stats_for_file(folder / file, file, stats)
    return stats
