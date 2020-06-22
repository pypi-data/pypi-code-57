from tokenizer_tools.tagset.offset.exceptions import OffsetSpanCheckError


class Span(object):
    """
    Basic unit for annotation. A span has `start`, `end`, `entity`, `value`.
    """

    def __init__(self, start, end, entity, value=None, normal_value=None):
        if start < 0:
            raise OffsetSpanCheckError("start index should greater or equal than zero")
        if end <= start:
            raise OffsetSpanCheckError("end is smaller than or equal to start")
        if not entity:
            raise OffsetSpanCheckError("'{}' is an illegal entity".format(entity))

        # compatible assert
        if value is not None:
            raise ValueError(
                "argument value={} is not supported anymore, ignore it".format(value)
            )

        self.start = start
        self.end = end
        self.entity = entity
        # self.value = value
        self.normal_value = normal_value

        # document that this span binding to
        self.host = None

    @property
    def value(self):
        if not self.host:
            return None
            # raise ValueError("This {} is not bind to Sequence".format(self.__class__.__name__))
        return self.host.text[self.start : self.end]

    def fetch_value_from_text(self, text):
        return text[self.start : self.end]

    @value.setter
    def value(self, new_value):
        self.update_value(new_value)

    def update_value(self, new_value):
        self.host.text[self.start : self.end] = new_value
        self.end = self.start + len(new_value)

    def check_match(self, text):
        if self.end > len(text):
            # raise OffsetSpanCheckError("end index should less or equal than lenght of text")
            return False

        if self.value is None:  # no value provide so skip match test
            return True

        matched_text = text[self.start : self.end]

        if matched_text != self.value:
            return False

        return True

    def fill_text(self, text):
        if not self.check_match(text):
            raise ValueError()

        matched_text = text[self.start : self.end]

        self.value = matched_text

    def bind(self, host):
        self.host = host

    def __deepcopy__(self, memodict={}):
        # not bind info
        return self.__class__(start=self.start, end=self.end, entity=self.entity)

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, value={!r}, normal_value={!r})".format(
            self.__class__.__name__,
            self.start,
            self.end,
            self.entity,
            self.value,
            self.normal_value,
        )

    def __hash__(self):
        return hash((self.start, self.end, self.entity))

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            and self.entity == other.entity
        )


if __name__ == "__main__":
    span = Span(0, 9, "entity")
    print(repr(span))
    assert repr(span) == "Span(0, 9, 'entity')"

    # span = Span(0, 0, 'entity')
    #
    # span = Span(1, 0, 'entity')
