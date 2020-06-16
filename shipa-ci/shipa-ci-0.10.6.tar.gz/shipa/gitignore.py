#
#  Copyright (c) 2019 Shipa authors
#
#  It's a python version of https://github.com/sabhiram/go-gitignore
#  Copyright (c) 2015 Shaba Abhiram
#

import re


def get_pattern_from_line(line):
    negative_pattern = False
    line = line.strip()

    # Strip comments [Rule 2]
    if line.startswith('#'):
        return None, None

    # Exit for no-ops and return nil which will prevent us from
    # appending a pattern against this line
    if len(line) == 0:
        return None, None

    # TODO: Handle [Rule 4] which negates the match for patterns leading with '!'
    if line[0] == '!':
        negative_pattern = True
        line = line[1:]

    # Handle [Rule 2, 4], when # or ! is escaped with a \
    # Handle [Rule 4] once we tag negatePattern, strip the leading ! char
    if re.compile(r'^(\#|\!)').match(line):
        line = line[1:]

    # Handle escaping the '.' char
    line = re.compile(r'\.').sub('\.', line)

    magicStar = '#$~'

    # Handle '/**/' usage
    if line.startswith('/**/'):
        line = line[1:]

    line = re.compile(r'/\*\*/').sub(r'(/|/.+/)', line)
    line = re.compile(r'\*\*/').sub(r'(|.'+magicStar+r'/)', line)
    line = re.compile(r'/\*\*').sub(r'(|/.'+magicStar+r')', line)
    #
    # // Handle escaping the '*' char
    line = re.compile(r'\\\*').sub(r'\\'+magicStar, line)
    line = re.compile(r'\*').sub(r'([^/]*)', line)
    #
    # // Handle escaping the '?' char
    line = line.replace('?', r'\?', -1)
    #
    line = line.replace(magicStar, '*')

    if line.endswith('/'):
        expr = line + r'(|.*)$'
    else:
        expr = line + r'(|/.*)$'

    if line.startswith('/'):
        expr = r'^(|/)' + expr[1:]
    else:
        expr = r'^(|.*/)' + expr

    pattern = re.compile(expr)
    return pattern, negative_pattern


class GitIgnore(object):

    def __init__(self, lines):
        self.items = []
        for line in lines:
            pattern, negative = get_pattern_from_line(line)
            if pattern is not None:
                self.items.append((pattern, negative))

    def match(self, path):
        matches = False
        for pattern, negative in self.items:
            m = re.match(pattern, path)
            if m:
                if negative is False:
                    matches = True
                elif matches:
                    matches = False
        return matches

