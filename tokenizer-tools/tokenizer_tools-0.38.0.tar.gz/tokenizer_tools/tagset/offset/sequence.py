import uuid
from typing import Union, Any, Mapping, List, Callable

from tokenizer_tools.tagset.offset.span_set import SpanSet
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.document_compare_ways import corpus_get_compare_way


class Sequence(object):
    """
    A implement of example which means this object is the basic element of model/training/test

    A sequence object has `text`, `span_set`, `id`, `label`, `extra_attr`.
    * `text` is a list of str (single char for char level application, multi char string for word level application)
    * `span_set` is a sparse annotation of this sequence.
    * `id` is the unique id of this sequence, can be used for tracing.
    * `label` the label of this sequence, used for classification.
    """

    def __init__(
        self,
        text: Union[List[str], str],
        span_set: SpanSet = None,
        id: Union[str, None] = None,
        label: Union[str, None] = None,
        extra_attr: Union[Mapping[str, Any], None] = None,
    ):
        # TODO:
        #   1. rename extra_attr to attr
        #   2. move label into attr
        #   3. span_set should include in some column data

        # convert text from string to list, if needed
        if isinstance(text, str):
            text = list(i for i in text)

        self.text = text
        self._span_set = None
        self.span_set = span_set or SpanSet()
        self.id = id if id is not None else str(uuid.uuid4())
        self.label = label  # for feature usage
        self.extra_attr = extra_attr if extra_attr else {}

        self._compare_method = None
        self._hash_method = None

    @property
    def span_set(self):
        return self._span_set

    @span_set.setter
    def span_set(self, value):
        self._span_set = value

        # binding now
        self._span_set.bind(self)

    @property
    def compare_method(self):
        if self._compare_method:
            return self._compare_method

        global_method = corpus_get_compare_way()
        return global_method["eq"]

    @compare_method.setter
    def compare_method(self, value):
        self._compare_method = value

    @property
    def hash_method(self):
        if self._hash_method:
            return self._hash_method

        global_method = corpus_get_compare_way()
        return global_method["hash"]

    @hash_method.setter
    def hash_method(self, value):
        self._hash_method = value

        self.span_set.bind(self)

    def add_extra_attr(self, **kwargs):
        self.extra_attr = kwargs

    def add_span(self, span):
        pass

    def check_span_set(self):
        """
        Check if span set match with sequence
        :return: bool
        """
        check_overlap, overlapped_result = self.span_set.check_overlap()
        # check_match, mismatch_result = self.span_set.check_match(self.text)

        # return check_overlap and check_match, overlapped_result, mismatch_result
        return check_overlap, overlapped_result

    def set_compare_method(
        self, compare_method: Callable[["Sequence", "Sequence"], bool]
    ):
        self.compare_method = compare_method

    def set_hash_method(self, hash_method: Callable[["Sequence"], int]):
        self.hash_method = hash_method

    @staticmethod
    def _default_compare_method(self, other):
        return (
            self.text == other.text
            and self.span_set == other.span_set
            and self.extra_attr == other.extra_attr
        )

    @staticmethod
    def _default_hash_method(self):
        return hash((frozenset(self.text), self.span_set, self.label))

    def __eq__(self, other):
        return self.compare_method(self, other)

    def __hash__(self):
        return self.hash_method(self)

    def __repr__(self):
        return "{}(text={!r}, span_set={!r}, id={!r}, label={!r}, extra_attr={!r})".format(
            self.__class__.__name__,
            self.text,
            self.span_set,
            self.id,
            self.label,
            self.extra_attr,
        )


if __name__ == "__main__":
    seq = Sequence("王小明在北京的清华大学读书。")
    seq.span_set.append(Span(0, 3, "PERSON", "王小明"))
    seq.span_set.append(Span(4, 6, "GPE", "北京"))
    seq.span_set.append(Span(7, 11, "ORG", "清华大学"))

    check_result = seq.check_span_set()
    print(check_result)
