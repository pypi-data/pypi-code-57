from tokenizer_tools.tagset.converter.offset_to_biluo import offset_to_biluo
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span
import pytest


@pytest.mark.skip("")
def test_offset_to_biluo():
    """seq = Document("王小明在北京的清华大学读书。")
    seq.span_set.append(Span(0, 3, 'PERSON', '王小明'))
    seq.span_set.append(Span(4, 6, 'GPE', '北京'))
    seq.span_set.append(Span(7, 11, 'ORG', '清华大学'))"""

    seq = ["B-I", "I-O"]

    # check_result = seq.check_span_set()
    # print(check_result)

    encoding = offset_to_biluo(seq)
    print(encoding)
