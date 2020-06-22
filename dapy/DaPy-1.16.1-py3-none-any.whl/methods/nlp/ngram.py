from ..core.base import BaseEngineModel
from .utils import get_ngram


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
        return get_ngram(input, *self._ngram)
