from collections import defaultdict
from typing import Set


class Statistics:
    def __init__(self):
        self.space_dict = defaultdict(int)
        self.tab_dict = defaultdict(int)
        self.mixed_line_dict = defaultdict(int)
        self.mixed_files: Set[str] = set()
        self.all_tabs = 0
        self.all_spaces = 0
        self.all_mixed = 0

    def add_spaces(self, extension='', count=1):
        self.space_dict[extension] += count
        self.all_spaces += count

    def add_tabs(self, extension='', count=1):
        self.tab_dict[extension] += count
        self.all_tabs += count

    def add_mixed_line(self, extension='', count=1, filename=''):
        self.mixed_line_dict[extension] += count
        self.mixed_files.add(filename)
        self.all_mixed += count
