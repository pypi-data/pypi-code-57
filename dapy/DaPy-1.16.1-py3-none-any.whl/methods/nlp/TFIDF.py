from collections import Counter, defaultdict
from heapq import nlargest
from math import log2
from operator import itemgetter

from .ngram import BaseNgramModel
from .utils import count_iter

ITEMGETTER1 = itemgetter(1)
ITEMGETTER0 = itemgetter(0)

class TfidfCounter(BaseNgramModel):
    def __init__(self, ngram=2, engine='numpy'):
        BaseNgramModel.__init__(self, ngram, engine)
        self.tfidf = {}

    @property
    def tfidf(self):
        return self._tfidf

    @tfidf.setter
    def tfidf(self, val):
        assert isinstance(val, dict)
        assert all(map(lambda v: isinstance(v, (float, int)), val.values())), 'values in the tfidf dict must be all int'    
        self._tfidf = val

    def __setstate__(self, args):
        BaseNgramModel.__setstate__(self, args)
        self.tfidf = args['_tfidf']

    def __getitem__(self, key):
        return self._tfidf[key]

    def _nlargest(self, n):
        return nlargest(n, self.tfidf.items(), key=ITEMGETTER1)

    def nlargest(self, n):
        return dict(self._nlargest(n))
        
    def fit(self, documents, labels=None, min_freq=1.0, min_document_ratio=0.0):
        if labels is None:
            labels = list(range(len(documents)))
        assert len(documents) == len(labels), 'number of documents must equal to number of labels'
        
        num_words = 0.0
        count_ngram = defaultdict(Counter)
        for row, label in zip(documents, labels):
            for pair in self._get_ngram(row):
                count_ngram[pair][label] += 1
                num_words += 1.0

        labels = Counter(labels)
        for label, freq in labels.items():
            labels[label] = freq * min_document_ratio
        
        selector = lambda value: value[1] >= labels[value[0]]
        self.tfidf, D = {}, len(labels) + 1.0
        for pair, counts in count_ngram.items():
            num_word = sum(counts.values())
            if num_word >= min_freq:
                tf = num_word / num_words
                df = count_iter(filter(selector, counts.items())) + 1.0
                self.tfidf[pair] = tf * log2(D / df)
        return self

    def transform(self, documents, max_num_tokens=500):
        tokens = map(ITEMGETTER0, self._nlargest(max_num_tokens))
        tokens = dict((token, index) for index, token in enumerate(tokens))
        shape = len(tokens)
        
        embeddings = []
        for row in documents:
            embedding = [0.0] * shape
            for pair in self._get_ngram(row):
                if pair in tokens:
                    embedding[tokens[pair]] += 1
            embeddings.append(embedding)
        return self._engine.vstack(embeddings)

    def fit_transform(self, documents, labels=None, min_freq=1.0, min_document_ratio=0.01, max_num_tokens=500):
        self.fit(documents, labels, min_freq, min_document_ratio)
        return self.transform(documents, max_num_tokens)

    def get(self, key, default=None):
        return self._tfidf.get(key, default)
