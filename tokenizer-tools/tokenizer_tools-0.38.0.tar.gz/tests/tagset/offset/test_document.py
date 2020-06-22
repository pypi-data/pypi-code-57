from tokenizer_tools.tagset.offset.corpus import Corpus


def test_attr_access(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    assert doc.domain == "domain"
    assert doc.function == "function"
    assert doc.intent == "intent"
    assert doc.sub_function == "sub_function"


def test_attr_change(datadir, tmpdir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    # change attr
    doc.domain = "DOMAIN"
    doc.function = "FUNCTION"
    doc.intent = "INTENT"
    doc.sub_function = "SUB_FUNCTION"

    # write out
    output_file = tmpdir / "data.conllx"
    corpus.write_to_file(output_file)

    # read in
    check_corpus = Corpus.read_from_file(output_file)
    check_doc = check_corpus[0]

    # check
    assert check_doc.domain == "DOMAIN"
    assert check_doc.function == "FUNCTION"
    assert check_doc.intent == "INTENT"
    assert check_doc.sub_function == "SUB_FUNCTION"


def test_as_string(datadir):
    corpus = Corpus.read_from_file(datadir / "corpus.conllx")
    doc = corpus[0]

    doc_string = str(doc)

    expected_doc_string = (
        "<D: domain, F: function, S: sub_function, I: intent>"
        "    "
        "[王小明](PERSON)在[北京](GPE)的[清华大学](ORG)读书。"
    )

    assert doc_string == expected_doc_string
