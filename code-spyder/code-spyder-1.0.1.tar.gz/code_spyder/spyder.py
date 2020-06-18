from os import listdir
from pathlib import Path

from interutils import pr, count_lines
from prettytable import PrettyTable


class Spyder:
    def __init__(self, target_dir: Path = Path.cwd(), depth: int = -1, exclude: iter = (),
                 inc_df: bool = False, suf_inc: iter = (), suf_exc: iter = ()):
        # Validate target
        self.target = Path(
            target_dir if target_dir else Path.cwd())

        # Crawl options
        self.exclude = exclude if exclude else list()
        self.inc_df = inc_df

        # Suffixes
        self.exc_suffixes = bool(suf_exc)
        self.suffixes = suf_exc if self.exc_suffixes else suf_inc

        # Crawl
        self.results = self.crawl_tree(self.target, int(depth))

    def summary(self, ignore_suffixes=False) -> str:
        # Create a table
        headers = ['Filename']
        headers += [] if ignore_suffixes else ['Suffix']
        headers += ['Lines']
        pt = PrettyTable(headers)

        if ignore_suffixes:
            # By lc only
            files = {}
            for suf, f in self.results.items():
                files.update(f)
            for k, v in sorted(files.items(), key=lambda item: item[1]):
                pt.add_row((k, v))
            pt.add_row(('Total Line Count', sum(files.values())))

        else:
            # By suffix and lc
            all_sum = 0
            for suf, files in self.results.items():
                for k, v in sorted(files.items(), key=lambda item: item[1]):
                    pt.add_row((k, suf,  v))
                suf_sum = sum(files.values())
                all_sum += suf_sum
                pt.add_row(('Total Line Count', suf,  suf_sum))
            pt.add_row(('Total Line Count', '*',  all_sum))
        return pt

    def crawl_tree(self, directory: Path, depth: int) -> dict:
        total = {}
        for file_name in listdir(directory):
            # Discard some
            if file_name in self.exclude:
                continue
            if not self.inc_df and file_name.startswith('.'):
                continue
            path = directory.joinpath(file_name)

            # If subpath is a dir - go deeper
            if path.is_dir():
                if depth == 0:
                    continue
                try:
                    sub_results = self.crawl_tree(path, depth-1)
                    # Merge subdir results with this-level's ones
                    for suf, v in sub_results.items():
                        if suf not in total:
                            total[suf] = {}
                        total[suf] = {**total[suf], **v}
                except (PermissionError, OSError) as e:
                    pr(f'Error "{e}" in directory: "{path}"', '!')
                continue

            # Check suffix
            suf = path.suffix[1:]  # Get last suffix without dot
            if self.exc_suffixes:
                if suf in self.suffixes:
                    continue
            else:
                if self.suffixes and suf not in self.suffixes:
                    continue

            # Update total
            try:
                lc = count_lines(path)
            except (PermissionError, OSError) as e:
                pr(f'Error "{e}" in file: "{path}"', '!')
                continue
            if suf not in total:
                total[suf] = {}
            total[suf][path.relative_to(self.target)] = lc

        return total
