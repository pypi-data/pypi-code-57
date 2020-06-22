import collections
import copy
import itertools
from typing import List

from tokenizer_tools.tagset.offset.span import Span


class SpanSet(List[Span]):
    """
    A annotation for example is a SpanSet.
     SpanSet is a unordered list. each element is a span which is basic annotaion unit.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # document this object binding to
        self.host = None

    @staticmethod
    def _are_separate(r: Span, s: Span) -> bool:
        # learned from https://stackoverflow.com/questions/27182137/check-if-two-lines-each-with-start-end-positions-overlap-in-python
        return r.end <= s.start or s.end <= r.start

    def check_overlap(self):
        """
        if overlap return False, otherwise return True
        :return: bool
        """

        comb = list(itertools.combinations(self, 2))

        test_results = list(map(lambda x: self._are_separate(*x), comb))

        if not all(test_results):
            overlapped_list = [comb[i] for i, v in enumerate(test_results) if not v]

            return False, overlapped_list

        return True, []

    @property
    def ordered_spans(self):
        assert self.check_overlap()

        return sorted(self, key=lambda x: x.start)

    def check_match(self, text):
        test_results = list(map(lambda x: x.check_match(text), self))

        if not all(test_results):
            mismatch_list = [self[i] for i, v in enumerate(test_results) if not v]

            return False, mismatch_list

        return True, []

    def bind(self, host):
        self.host = host

        for span in self:
            span.bind(host)

        # self.fill_text(host.text)

    def append(self, span) -> None:
        # override append method of list class
        super().append(span)
        span.bind(self.host)

    def __deepcopy__(self, memodict={}):
        # not bind info
        return self.__class__([copy.deepcopy(span) for span in self])

    def fill_text(self, text):
        flag, _ = self.check_match(text)

        if not flag:
            raise ValueError()

        for span in self:
            span.fill_text(text)

    def __hash__(self):
        return hash(frozenset(self))

    def __eq__(self, other):
        return collections.Counter(self) == collections.Counter(other)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, list(self))
