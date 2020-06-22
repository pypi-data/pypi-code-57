from tokenizer_tools.conllz.reader import read_conllx_from_string, read_conllx, load_conllx
import pytest


@pytest.mark.skip("")
def test_read_conllx_from_string():
    # TODO this way to test has no affect?
    for i in read_conllx_from_string("today is a happy day"):
        print("read_conllz_from_string:", i)


@pytest.mark.skip("")
def test_read_conllx_from_string():
    for i in read_conllx_from_string(" the weather is nice"):
        print("read_conllz_from_string:", i)


def test_read_conllx(datadir):
    with open(datadir / "corpus.conllx") as fd:
        result = read_conllx(fd)
    assert len(result) == 3

    # result[2] expected to be ['A', ' ', 'c', 'a', 'r']
    assert len(result[2].word_lines) == 5
    assert result[2].word_lines[1] == " "

def test_load_conllx(datadir):
    with open(datadir / "corpus.conllx") as fd:
        result = list(load_conllx(fd))
        assert len(result) == 3

        # result[2] expected to be ['A', ' ', 'c', 'a', 'r']
        assert len(result[2].word_lines) == 5
        assert result[2].word_lines[1] == " "


@pytest.mark.skip("not ready")
def test_load_conllx_with_linenum_in_exception(datadir):
    # with open(datadir / "corpus.conllx") as fd:
    #     data = fd.read()

    # result = load_conllx(data)
    pass
