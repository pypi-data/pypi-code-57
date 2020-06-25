import re
from copy import copy


class Negation:

    def __init__(self, term, match):
        self._term = term
        self._match = match

    @property
    def match(self):
        if isinstance(self._match, re.Match):
            return self._match.group()
        return str(self._match)

    @property
    def term(self):
        if isinstance(self._term, re.Pattern):
            return self._term.pattern
        return str(self._term)


class Match:

    def __init__(self, match, groups=None):
        self.match = match
        self._groups = groups

    def group(self, *index):
        if not self._groups or not index or len(index) == 1 and index[0] == 0:
            return self.match.group(*index)
        res = []
        if not isinstance(index, tuple):
            index = (index,)
        for idx in index:
            if idx == 0:
                res.append(self.match.group())
            else:
                res.append(self._groups[idx - 1])

    def groupdict(self, name=None, default=None):
        d = self.match.groupdict(default)
        return d[name] if name else d

    def groups(self):
        if not self._groups:
            return self.match.groups()
        else:
            return tuple(self._groups)

    def has_group(self, name, luetella=False):
        """

        :param name:
        :param luetella: enumerate if True or supply a maximum number
        :return:
        """
        if luetella:
            i = ''
            while True:
                if f'{name}{i}' in self.match.groupdict():
                    if self.match.groupdict()[f'{name}{i}']:
                        return True
                    elif i == '':
                        i = 0
                    else:
                        i += 1
                else:
                    return False
        return name in self.match.groupdict() and self.match.groupdict()[name]


class Pattern:

    def __init__(self, pattern, negates=None, replace_whitespace=r'\W*',
                 capture_length=None, retain_groups=None,
                 flags=re.IGNORECASE):
        """

        :param pattern:
        :param negates:
        :param replace_whitespace:
        :param capture_length: for 'or:d' patterns, this is the number
            of actual capture groups (?:(this)|(that)|(thes))
            has capture_length = 1
            None: i.e., capture_length == max
        :param flags:
        """
        self.match_count = 0
        if replace_whitespace:
            pattern = replace_whitespace.join(pattern.split(' '))
        if retain_groups:
            for m in re.finditer(r'\?P<(\w+)>', pattern):
                term = m.group(1)
                if term in retain_groups:
                    continue
                pattern = re.sub(f'\\?P<{term}>', r'\?:', pattern)
        self.pattern = re.compile(pattern, flags)
        self.negates = []
        for negate in negates or []:
            if replace_whitespace:
                negate = replace_whitespace.join(negate.split(' '))
            self.negates.append(re.compile(negate, flags))
        self.capture_length = capture_length
        self.text = self.pattern.pattern

    def __str__(self):
        return self.text

    def matches(self, text, ignore_negation=False, return_negation=False):
        m = self.pattern.search(text)
        if m:
            if not ignore_negation:
                for negate in self.negates:
                    if negate.search(text):
                        return Negation(negate, m) if return_negation else False
            self.match_count += 1
            return Match(m, groups=self._compress_groups(m))
        return False

    def _compress_groups(self, m):
        if self.capture_length:
            groups = m.groups()
            assert len(groups) % self.capture_length == 0
            for x in zip(*[iter(m.groups())] * self.capture_length):
                if x[0] is None:
                    continue
                else:
                    return x
        else:
            return None

    def matchgroup(self, text, index=0):
        m = self.matches(text)
        if m:
            return m.group(index)
        return m

    def sub(self, repl, text):
        return self.pattern.sub(repl, text)

    def next(self, text, **kwargs):
        m = self.pattern.search(text, **kwargs)
        if m:
            self.match_count += 1
            return text[m.end():]
        return text


class MatchCask:

    def __init__(self):
        self.matches = []

    def add(self, m):
        self.matches.append(m)

    def add_all(self, matches):
        self.matches += matches

    def copy(self):
        mc = MatchCask()
        mc.matches = copy(self.matches)
        return mc

    def __repr__(self):
        return repr(set(m.group() for m in self.matches))

    def __str__(self):
        return str(set(m.group() for m in self.matches))
