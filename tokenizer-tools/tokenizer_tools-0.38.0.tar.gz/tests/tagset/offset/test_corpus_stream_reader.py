import filecmp
import tempfile
from pathlib import Path

from tokenizer_tools.tagset.offset.corpus import Corpus


def test_reader(datadir):
    data_file = datadir / "data.conllx"
    expected_docs = [doc for doc in Corpus.read_from_file(data_file)]

    result_docs = []
    with Corpus.stream_reader(data_file) as docs_generator:
        for doc in docs_generator:
            result_docs.append(doc)

    assert result_docs == expected_docs
