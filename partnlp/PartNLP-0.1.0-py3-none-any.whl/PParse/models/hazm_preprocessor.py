"""Using Hazm to preprocessing the persian data.
"""
from __future__ import unicode_literals
from hazm import Stemmer, Normalizer, Lemmatizer
from PPars.models.preprocess import PreProcess
import hazm


class HAZMPreprocessor(PreProcess):
    """Initialize its constructor using parent constructor.
    """
    def __init__(self, config=None):
        super().__init__(config)
        self.model = hazm

    def normalizer(self):
        normalizer = Normalizer()
        self.data = normalizer.normalize(self.data)

    def stem(self):
        """
        :return:
        """
        stemmer = Stemmer()
        for words in self.words:
            temp = []
            for word in words:
                temp.append(stemmer.stem(str(word)))
            self.stem_words.append(temp)
        print('the result of stemming is = {}'.format(self.stem_words))

    def lemmatize(self):
        """
        :return:
        """
        lemmatizer = Lemmatizer()
        for words in self.words:
            temp = []
            for word in words:
                temp.append(lemmatizer.lemmatize(str(word)))
            self.lemmatized_words.append(temp)
        print('the result of lemmatizing is = {}'.format(self.lemmatized_words))
