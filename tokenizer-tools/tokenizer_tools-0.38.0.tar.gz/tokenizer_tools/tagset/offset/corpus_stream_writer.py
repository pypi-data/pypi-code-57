from tokenizer_tools.converter.offset_to_sentence import offset_to_sentence
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.conllz.writer import write_conllx


class CorpusStreamWriter:
    def __init__(self, file_path):
        self.fd = open(file_path, "wt")

    def write(self, doc: Document):
        sentence = offset_to_sentence(doc)

        write_conllx([sentence], self.fd)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close_opened_file()

    def close_opened_file(self):
        self.fd.close()
