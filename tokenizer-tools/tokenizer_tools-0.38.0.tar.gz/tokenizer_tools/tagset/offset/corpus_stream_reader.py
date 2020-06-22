from tokenizer_tools.conllz.reader import load_conllx
from tokenizer_tools.converter.conllx_to_offset import conllx_to_offset


class CorpusStreamReader:
    def __init__(self, file_path):
        self.fd = open(file_path, "rt")

    def doc_generator(self):
        for sentence in load_conllx(self.fd):
            offset_data, result = conllx_to_offset(sentence)
            yield offset_data

    def __enter__(self):
        return self.doc_generator()

    def __exit__(self, type_, value, traceback):
        self.close_opened_file()

    def close_opened_file(self):
        self.fd.close()
