from collections import Counter, defaultdict
from heapq import nlargest
from math import log2
from functools import reduce
from operator import itemgetter, mul
from .base import BaseEngineModel

HEAD = '<HEAD>'
END = '<END>'
OOV = '<OOV>'


def count_iter(iterable):
    count = 0.0
    while True:
        try:
            next(iterable)
        except StopIteration:
            return count
        count += 1.0


class BaseNgramModel(BaseEngineModel):

    def __init__(self, ngram=2, engine='numpy'):
        BaseEngineModel.__init__(self, engine)
        self.ngram = ngram

    def __setstate__(self, args):
        BaseEngineModel.__setstate__(self, args)
        self.ngram = args['_ngram']

    @property
    def ngram(self):
        return self._ngram

    @ngram.setter
    def ngram(self, new_ngram):
        assert isinstance(new_ngram, (tuple, int, list)), 'n_gram parameter must be int or tuple'
        if isinstance(new_ngram, int):
            assert new_ngram >= 1, 'n_gram parameter must greater than 1'
            self._ngram = (new_ngram, new_ngram)

        if isinstance(new_ngram, (tuple, list)):
            error = 'n_gram parameter must two numbers in a tuple'
            assert len(new_ngram) == 2, error
            num1, num2 = new_ngram
            assert isinstance(num1, int) and num1 >= 1, error
            assert isinstance(num2, int) and num2 > num1, error
            self._ngram = (num1, num2)

    def _get_ngram(self, input):
        input = list(input)
        length = len(input)
        input.extend(repeat(END, self._ngram[1]))
        input = tuple(input)
        for n in range(self._ngram[0]-1, self._ngram[1]):
            for k in range(1, 1 + n):
                yield (HEAD,) * k + input[:n-k+1]
            for i in range(length):
                yield input[i: i+1+n]



            


class LanguageModel(BaseNgramModel):
    
    __name__ = 'N-Gram Language Model'

    def __init__(self, ngram=2, engine='numpy'):
        BaseNgramModel.__init__(self, ngram, engine)
        self.tf = Counter()

    @property
    def tf(self):
        return self._tf

    @tf.setter
    def tf(self, val):
        assert isinstance(val, dict)
        assert all(map(lambda v: isinstance(v, (float, int)), val.values())), 'values in the tf dict must be all int'    
        self._tf = val
        
    def __setstate__(self, args):
        BaseNgramModel.__setstate__(self, args)
        self.tf = args['_tf']

    def _nlargest(self, n):
        return nlargest(n, self.tf.items(), key=ITEMGETTER1)

    def nlargest(self, n):
        return dict(self._nlargest(n))

    def fit(self, documents, min_freq=1.0):
        num_ngram = Counter()
        for row in documents:
            num_ngram.update(self._get_ngram(row))

        remove_min_freq = filter(lambda val: val >= min_freq, num_ngram.values())
        num_words = sum(remove_min_freq, 1.0)
        self.tf = {OOV: 1.0 / num_words}
        for pair, counts in num_ngram.items():
            if counts >= min_freq:
                self._tf[pair] = (counts + 1.0) / num_words
        return self.tf

    def predict(self, documents):
        return [self.predict_once(row) for row in documents]
    
    def predict_once(self, sentence):
        oov = self.tf[OOV]
        ngrams = self._get_ngram(sentence)
        return reduce(mul, [self.tf.get(_, oov) for _ in ngrams], 1.0)
