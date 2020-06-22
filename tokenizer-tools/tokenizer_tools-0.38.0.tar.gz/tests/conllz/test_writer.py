from tokenizer_tools.conllz.sentence import SentenceX
from tokenizer_tools.conllz.writer import write_conllx


# write text to file, what's the structure need?
def test_write_conllx():
    sentence_1 = SentenceX()
    sentence_1.id = "SID-1"
    sentence_1.write_as_row(["char-1", "tag-1"])
    sentence_1.write_as_row(["char-2", "tag-2"])

    sentence_2 = SentenceX()
    sentence_2.id = "SID-2"
    sentence_2.write_as_row(["char-1", "tag-1"])
    sentence_2.write_as_row(["char-2", "tag-2"])

    sentence = [sentence_1, sentence_2]
    write_conllx(sentence, open("corpus4.txt", "w"))
