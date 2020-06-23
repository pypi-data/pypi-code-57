"""

IDE: PyCharm
Project: RobiNLP
Author: Robin
Filename: nlp_utils.py
Date: 23.06.2020

"""


def extract_ngrams(text: str, ngram_size: int = 2, tokenizer=None):
    if tokenizer is None:
        tokens = text.split()
    else:
        tokens = tokenizer(text)

    ngrams = []
    for i in range(0, len(tokens), ngram_size):
        ngrams.append(" ".join(tokens[i:i + ngram_size]))
    return ngrams
