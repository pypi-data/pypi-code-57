from .processing import CorpusHandler
# from pre_processing.pre_processing import CorpusHandler


# def preprocess(text):
#     text_process = CorpusHandler.clean_corpus(text)
#
#     return text_process

def clean(text):
    text = text.lower()

    text = CorpusHandler.clean_email(text)
    text = CorpusHandler.clean_site(text)
    text = CorpusHandler.transform_token(text)
    text = CorpusHandler.clean_special_chars(text)
    text = CorpusHandler.remove_letter_number(text)
    text = CorpusHandler.clean_number(text)
    text = CorpusHandler.clean_alphachars(text)
    text = CorpusHandler.clean_document(text)
    text = CorpusHandler.remove_stop_words(text)
    text = text.split()
    text = ' '.join([x for x in text if len(x) > 2])
    text = CorpusHandler.clean_spaces(text)

    return text


def preprocess(text):
    # text_process = CorpusHandler.preprocess(
    #     text,
    #     disabled=[
    #               'to_st_named_entities',
    #               'spellchecker',
    #               'lemmatize',
    #               'tokenize']
    # )

    return clean(text)
