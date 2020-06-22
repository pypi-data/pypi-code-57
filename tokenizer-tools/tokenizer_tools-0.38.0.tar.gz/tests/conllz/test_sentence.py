from tokenizer_tools.conllz.sentence import Sentence, SentenceX
import pytest


@pytest.mark.skip("")
def test_write_as_row():
    s = Sentence(["1"], ["cfv", "dddwedwf"], ["cfv"], 4)
    data = ["a", "b", "c"]
    s.write_as_row(data)
    print(s)


def test_init():
    s = Sentence(1, 2, 3, 4)
    assert (
        s.id == 4
        and s.attribute_names == 3
        and s.attribute_lines == 2
        and s.word_lines == 1
    )


def test_get_attribute():
    s = Sentence(1, ["2", 3], 3, 4)
    d = s.get_attribute(1)
    print(d)
