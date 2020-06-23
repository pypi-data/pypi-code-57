"""Using Parsivar to preprocessing the persian text.
"""
from parsivar import Normalizer, FindStems
from mPPars.models.hazm_preprocessor import PreProcess
from mPPars.models.constants.color import Color
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
        print(f'{Color.HEADER} Sent_Tokenize: {Color.ENDC} {Color.BLUE}{self.sentences}{Color.ENDC}')

    def word_tokenize(self):
        self.words = [self.model.Tokenizer().tokenize_words(sent) for sent in self.sentences]
        print(f'{Color.HEADER} Word_tokenize: {Color.ENDC} {Color.BLUE}{self.words}{Color.ENDC}')

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
        print(f'{Color.HEADER} Stem_Words: {Color.ENDC} {Color.BLUE}{self.stem_words}{Color.ENDC}')


