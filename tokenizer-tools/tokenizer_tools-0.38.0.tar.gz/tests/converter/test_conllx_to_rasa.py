from tokenizer_tools.converter.conllx_to_rasa import conllx_to_rasa
import pytest


@pytest.mark.skip("")
def test_conllx_to_rasa(datadir):
    rs = conllx_to_rasa(datadir / "1.txt", datadir / "2.txt")
    print(rs)
