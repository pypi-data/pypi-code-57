from tokenizer_tools.converter.conllx_to_offset import conllx_to_offset
from tokenizer_tools.conllz.sentence import SentenceX
import pytest


@pytest.mark.skip("")
def test_conllx_to_offset():
    sentence = SentenceX()
    sentence.attribute_lines["0", "3", "8"]
    sentence.attribute_names["B-I", "B-L", "B-0"]
    rs = conllx_to_offset(sentence)
    print(rs)
