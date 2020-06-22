import re

import astunparse
import ast
import attr

from .renderer import render_with_identifiers, parse_identifiers
from .skeleton import Skeleton, Blank, Given


@attr.s
class Reskeletonizer:
    ignore_whitespace = attr.ib(default=False)
    normalizer = attr.ib(default=None)
    """
    Reskeletonizer that uses character-level matching to match given portions the skeleton
        in the provided code, in order to find blanks.

    Arguments
        ignore_whitespace: whether to ignore whitespace when resolving blanks. Default False
        normalizer: function that parses and unparses code, to remove extraneous formatting.
            Default is None, or no normalization. If this is used, the returned reskeletonized
            code will correspond to the normalized code rather than the original code.
            
            For this to work, the blanks in the original skeleton must correspond to places an
            identifier could be placed, syntactically. Additionally, any sequence of [a-z]*
            must be a valid identifier for this to work.
    """

    def reskeletonize(self, skeleton: Skeleton, code: str) -> Skeleton:
        if self.normalizer is not None:
            code = self.normalizer(code)
            skeleton_code, skeleton_ids = render_with_identifiers(skeleton)
            skeleton_code = self.normalizer(skeleton_code)
            skeleton = parse_identifiers(skeleton_code, skeleton_ids)

        match = self.create_regex(skeleton).match(code)
        if not match:
            raise CannotReskeletonizeException

        blanks = match.groups()
        assert len(blanks) == len(skeleton.segments)

        new_segments = []
        for segment, content in zip(skeleton.segments, blanks):
            if isinstance(segment, Blank):
                new_segments.append(Blank(content))
            elif isinstance(segment, Given):
                new_segments.append(Given(content))
            else:
                raise AssertionError("Should be unreachable")

        return Skeleton(new_segments)

    def create_regex(self, skeleton):
        regex_chunks = ["^"]
        for segment in skeleton.segments:
            regex_chunks.append(segment.matcher_regex(self._match_given_text))
        regex_chunks.append("$")
        pattern = "".join(regex_chunks)
        return re.compile(pattern, re.DOTALL)

    def _match_given_text(self, code):
        if not self.ignore_whitespace:
            return re.escape(code)
        return r"\s+".join(re.escape(word) for word in re.split(r"\s", code))


def normalize_python(code):
    return astunparse.unparse(ast.parse(code, "<<code>>"))


class CannotReskeletonizeException(Exception):
    pass
