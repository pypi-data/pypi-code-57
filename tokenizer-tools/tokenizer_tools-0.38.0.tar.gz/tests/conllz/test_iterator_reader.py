from tokenizer_tools.conllz.iterator_reader import (
    read_conllx_iterator,
    read_conllx_from_string,
    conllx_iterator_reader,
)


def test_read_conllx_iterator(datadir):
    for i in read_conllx_iterator(datadir / "corpus1.txt"):
        print(i)


def test_conllx_iterator_reader(datadir):
    for i in conllx_iterator_reader([datadir / "corpus1.txt"]):
        print(i)
