import sys
from .read_input_helper import getch

def print_seperator(sep="_", count=120):
    print(sep*count)

def print_list(list:list):
    print(*list, sep="\n")

def strip(string):
    return string.strip()

def printf(*values,  sep=' ', end='\n', file=sys.stdout, flush=False, silent=False):
    if not silent:
        print(values=values, sep=sep, end=end, file=file, flush=flush)

def get_list_from_string(string, seperator="\n"):
    output_list = [item for item in string.split(seperator) if item != ""]
    return list(map(strip, output_list))

def replace_every_string(current_string, with_string, in_list:list):
    return list(map(lambda x: x.replace(current_string, with_string), in_list))