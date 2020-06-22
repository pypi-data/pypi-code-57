from typing import List
from tokenizer_tools.tagset.NER.base_tagset import BaseTagSet
from tokenizer_tools.tagset.exceptions import TagSetDecodeError
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet


def tags_to_span_set(tags: List[str]) -> SpanSet:
    decoder = BILUOSequenceEncoderDecoder()
    span_info = decoder.decode_to_offset(tags)

    return SpanSet([Span(i[0], i[1], i[2]) for i in span_info])


class BILUOEncoderDecoder(BaseTagSet):
    """
    Encoder and Decoder for BILUO scheme
    """

    # O is very easy confused with zero, using oscar instead in the code
    oscar = "O"

    def generate_tag(self, prefix):
        if self.tag_name == self.oscar:
            # O tag is very special, it always return O
            return self.oscar

        if self.tag_name is not None:
            tag = "{}-{}".format(prefix, self.tag_name)
        else:
            # if tag_name is None, no more tag_name in tag
            tag = prefix

        return tag

    def encode(self, sequence):
        len_of_sequence = len(sequence)

        if len_of_sequence == 1:
            return [self.generate_tag("U")]

        elif len_of_sequence == 2:
            return [self.generate_tag("B"), self.generate_tag("L")]

        else:
            return (
                [self.generate_tag("B")]
                + [self.generate_tag("I")] * (len_of_sequence - 2)
                + [self.generate_tag("L")]
            )

    def decode(self, sequence):
        pass

    def all_tag_set(self):
        tag_set = {self.generate_tag(i) for i in "BILU"}
        tag_set_oscar = {self.oscar}
        tag_set.update(tag_set_oscar)
        return tag_set


class BILUOSequenceEncoderDecoder(object):
    # O is very easy confused with zero, using oscar instead in the code
    oscar = "O"

    legal_set = {
        ("B", "I"),
        ("B", "L"),
        ("I", "I"),
        ("I", "L"),
        (oscar, "B"),
        ("L", oscar),
        (oscar, "U"),
        ("U", oscar),
        ("U", "B"),
        ("L", "U"),
        ("U", "U"),
    }

    prefix_set = set("BILU")

    def __init__(self, *args, **kwargs):
        self.ignore_error = kwargs.get("ignore_error", True)

    def parse_tag(self, tag):
        # TODO: already replaced by inline code, remove me in later version
        if tag == self.oscar:
            return self.oscar, None

        # set maxsplit to 1, so raw_tag_name can contains '-' char legally
        raw_prefix, raw_tag_name = tag.split("-", maxsplit=1)

        prefix = raw_prefix.strip()
        tag_name = raw_tag_name.strip()

        if prefix and tag_name and prefix in self.prefix_set:
            return prefix, tag_name

        raise ValueError("tag: {} is not a avoid tag".format(tag))

    def is_prefix_legal(self, previous, current):
        node = (previous, current)

        return node in self.legal_set

    def decode_to_offset(self, sequence):
        offset_list = []

        last_tag_prefix = None
        tag_length = 0
        tag_name_cache = None

        for index, item in enumerate(sequence):
            # inline function <<< self.parse_tag(item)
            tag = item
            if tag == self.oscar:
                prefix = self.oscar
                tag_name = None
            else:
                # set maxsplit to 1, so raw_tag_name can contains '-' char legally
                prefix, tag_name = tag.split("-", maxsplit=1)

                if prefix and tag_name and prefix in self.prefix_set:
                    pass
                else:
                    raise ValueError("tag: {} is not a avoid tag".format(tag))
            # inline function >>> self.parse_tag(item)

            if last_tag_prefix is None:
                if prefix == self.oscar:
                    # ignore it
                    continue
                elif prefix == "B":
                    tag_name_cache = tag_name
                    last_tag_prefix = prefix
                    tag_length += 1
                elif prefix == "U":
                    offset_list.append((index, index + 1, tag_name))
                else:
                    if not self.ignore_error:
                        raise TagSetDecodeError(
                            "sequence: {} is not a valid tag sequence".format(
                                sequence[: index + 1]
                            )
                        )
                    else:
                        continue
            else:
                if not self.is_prefix_legal(last_tag_prefix, prefix):
                    raise TagSetDecodeError(
                        "sequence: {} is not a valid tag sequence".format(
                            sequence[: index + 1]
                        )
                    )

                if prefix == "L":
                    if tag_name_cache == tag_name:
                        offset_list.append(
                            (index - tag_length, index + 1, tag_name_cache)
                        )

                        # clean up
                        last_tag_prefix = None
                        tag_length = 0
                        tag_name_cache = None
                    else:
                        raise TagSetDecodeError(
                            "sequence: {} is not a valid tag sequence".format(
                                sequence[: index + 1]
                            )
                        )
                elif prefix == "I":
                    if tag_name_cache == tag_name:
                        last_tag_prefix = prefix
                        tag_length += 1
                    else:
                        raise TagSetDecodeError(
                            "sequence: {} is not a valid tag sequence".format(
                                sequence[: index + 1]
                            )
                        )

        return offset_list

    def to_offset(self, sequence, text, **kwargs):
        span_set = SpanSet(
            [
                Span(offset[0], offset[1], offset[2])
                for offset in self.decode_to_offset(sequence)
            ]
        )

        label = kwargs.pop("label", None)
        id_ = kwargs.pop("id", None)
        extra_attr = kwargs

        seq = Document(text, span_set, id_, label, extra_attr)
        seq.span_set.bind(seq)

        return seq


if __name__ == "__main__":
    decoder = BILUOSequenceEncoderDecoder()
    result = decoder.decode_to_offset(["U-XX"])
    print(result)
    assert result == [(0, 1, "XX")]

    result = decoder.decode_to_offset(["U-XX", "U-YY"])
    print(result)
    assert result == [(0, 1, "XX"), (1, 2, "YY")]

    result = decoder.decode_to_offset(["B-XX", "I-XX", "L-XX"])
    print(result)
    assert result == [(0, 3, "XX")]
