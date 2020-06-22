from collections import Counter, defaultdict
from functools import reduce
from heapq import nlargest
from operator import itemgetter, mul


from .constant import OOV, END
from .ngram import BaseNgramModel
from .utils import get_left_padding

ITEMGETTER1 = itemgetter(1)

class LanguageModel(BaseNgramModel):
    
    __name__ = 'N-Gram Language Model'

    def __init__(self, ngram=2, term_frequency=None, engine='numpy'):
        BaseNgramModel.__init__(self, ngram + 1, engine)
        self.tf = term_frequency

    @property
    def tf(self):
        return self._tf

    @tf.setter
    def tf(self, val):
        if val is None:
            val = Counter()
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
        self.tf = defaultdict(lambda : Counter({OOV: 1.0}))
        for row in documents:
            for ngram in self._get_ngram(row):
                self.tf[ngram[:-1]][ngram[-1]] += 1

        total_words = 1.0
        to_remove = []
        for pair, counter in self.tf.items():
            words = sum(counter.values(), len(counter) - 1)
            if words >= min_freq:
                total_words += words
                counter[OOV] /= words
                for word in counter:
                    if word != OOV:
                        counter[word] = (counter[word] + 1) / words
            else:
                to_remove.append(pair)

        self.tf[OOV] = {OOV: 1.0 / total_words}
        for _ in to_remove:
            del self.tf[_]
        return self

    def predict_proba(self, documents):
        return [self._predict_proba(row) for row in documents]
    
    def _predict_proba(self, sentence):
        proba = 1.0
        oov_pair = self.tf[OOV]
        for times, ngram in enumerate(self._get_ngram(sentence), 1):
            before, word = ngram[:-1], ngram[-1]
            counter = self.tf.get(before, oov_pair)
            proba *= counter.get(word, counter[OOV])
        return proba ** (1.0 / times)

    def predict_words(self, documents):
        return [self._predict_words(row) for row in documents]

    def _predict_words(self, sentence):
        sentence = list(get_left_padding(sentence, self._ngram[1]))
        oov_pair = self.tf[OOV]
        word = sentence[-1]
        end_note = set([END, OOV])
        
        while word not in end_note:
            before = sentence[1-self._ngram[1]:]
            counter = self.tf.get(tuple(before), oov_pair)
            word = nlargest(1, counter.items(), ITEMGETTER1)[0][0]
            sentence.append(word)
        return sentence[self._ngram[1] + 1:-1]
