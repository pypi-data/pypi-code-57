"""Using Parsivar to preprocessing the persian text.
"""
from parsivar import Normalizer, FindStems
from PPars.models.hazm_preprocessor import PreProcess
import parsivar


class PARSIVARPreprocessor(PreProcess):
    """ PARSIVARPreprocessor
    """
    def __init__(self, config=None):
        # Initialize its constructor using parent constructor.
        super().__init__(config)
        self.model = parsivar

    def sent_tokenize(self):
        self.sentences = self.model.Tokenizer().tokenize_sentences(self.data)
        print('the result of sent tokenize is = {}'.format(self.sentences))

    def word_tokenize(self):
        self.words = [self.model.Tokenizer().tokenize_words(sent) for sent in self.sentences]
        print('the result of word tokenize is = {}'.format(self.words))

    def normalizer(self):
        """
        :return:
        """
        normalizer = Normalizer()
        self.data = normalizer.normalize(self.data)

    def stem(self):
        """
        :return:
        """
        stemmer = FindStems()
        for words in self.words:
            temp = []
            for word in words:
                temp.append(stemmer.convert_to_stem(str(word)))
            self.stem_words.append(temp)
        print('the result of stemming is = {}'.format(self.stem_words))


