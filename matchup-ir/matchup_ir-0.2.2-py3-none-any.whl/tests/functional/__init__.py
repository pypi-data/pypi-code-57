__all__ = ['boolean_test', 'extended_boolean_test', 'vector_test', 'probabilistic_test', 'main']

from matchup.structure.vocabulary import Vocabulary
from matchup.structure.query import Query


def set_up_txt_test():
    vocabulary = Vocabulary("./tests/static/files", stopwords="./tests/static/pt-br.txt")
    # vocabulary.import_collection()
    vocabulary.import_folder("./tests/static/files")
    vocabulary.index_files()
    vocabulary.save()
    query = Query(vocabulary=vocabulary)
    return vocabulary, query


def set_up_pdf_test():
    vocabulary = Vocabulary("./tests/static/pdf-files", stopwords="./tests/static/pt-br.txt")
    # vocabulary.import_collection()
    vocabulary.import_folder("./tests/static/pdf-files")
    vocabulary.index_files()
    vocabulary.save()
    query = Query(vocabulary=vocabulary)
    return vocabulary, query
