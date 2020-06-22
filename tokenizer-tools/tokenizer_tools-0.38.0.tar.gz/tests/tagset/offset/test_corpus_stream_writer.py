import filecmp
import tempfile
from pathlib import Path

from tokenizer_tools.tagset.offset.corpus import Corpus


def test_writer(datadir):
    src_file = datadir / "data.conllx"
    docs = Corpus.read_from_file(src_file)

    result_file = Path(tempfile.mkdtemp()) / "data.conllx"

    with Corpus.stream_writer(result_file) as writer:
        for doc in docs:
            writer.write(doc)

    assert filecmp.cmp(src_file, result_file, shallow=False)
