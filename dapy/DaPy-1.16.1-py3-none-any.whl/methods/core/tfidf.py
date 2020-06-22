from collections import Counter, defaultdict
from heapq import nlargest
from itertools import chain
from math import log10
from operator import itemgetter

from .base import BaseEngineModel

HEAD = '<HEAD>'
END = '<END>'
ITEMGETTER1 = itemgetter(1)
ITEMGETTER0 = itemgetter(0)

def count_iter(iterable):
    count = 0.0
    while True:
        try:
            next(iterable)
        except StopIteration:
            return count
        count += 1.0
        
class TfidfCounter(BaseEngineModel):
    def __init__(self, ngram=1, engine='numpy'):
        BaseEngineModel.__init__(self, engine)
        self.ngram = ngram
        self.tfidf = {}

    @property
    def ngram(self):
        return self._ngram

    @ngram.setter
    def ngram(self, num_words):
        assert isinstance(num_words, int), 'n_gram parameter must be int'
        assert num_words >= 1, 'n_gram parameter must greater than 1.'
        self._ngram = num_words
        self._h = (HEAD,) * (self.ngram - 1)
        self._e = (END,) * (self.ngram - 1)

    @property
    def tfidf(self):
        return self._tfidf

    @tfidf.setter
    def tfidf(self, values):
        assert isinstance(values, dict)
        self._tfidf = values
        
    def __setstate__(self, args):
        BaseEngineModel.__setstate__(self, args)
        self.ngram = args['_ngram']

    def _pad(self, string):
        return self._h + tuple(string) + self._e

    def _get_ngram(self, string):
        if self._ngram == 1:
            for token in string:
                yield token
        else:
            string = self._pad(string)
            for i in range(len(string) - self._ngram + 1):
                yield string[i:i+self._ngram]


if __name__ == '__main__':
    documents = [
        ['This', 'is', 'a', 'lucky', 'day'],
        ['This', 'is', 'not', 'a', 'lucky', 'day'],
        ]
    counter = TfidfCounter(2)
    print(counter.fit_transform(documents, [1, 0]))
    print(counter.tfidf)
