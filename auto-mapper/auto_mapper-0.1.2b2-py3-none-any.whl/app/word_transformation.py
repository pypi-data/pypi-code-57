from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from mapper.utils.common import deprecated

import re
import string
import unidecode

class WordTransformation:
  CP_CASE_EXP = '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
  KB_CASE_EXP = '[_-]'
  PUNCTUATION_TABLE = str.maketrans('', '', string.punctuation)

  def __init__(self, stop_word=False, use_stemmer=False, lang='english'):
    if stop_word == True:
      stop_words = stopwords.words('english') + stopwords.words('french') + stopwords.words('german')
      self.stop_words = set(stop_words)
    
    if use_stemmer == True:
      self.stemmer = SnowballStemmer(language=lang)

  def lower(self, word):
    return word.lower()
  
  @deprecated("This method is deprecated, it'll be removed in the next release")
  def is_stop_word(self, word):
    if not hasattr(self, 'stop_words'):
      return False
    
    return self.lower(word) in self.stop_words
  
  def remove_punctuation(self, word):
    return word.translate(self.PUNCTUATION_TABLE)
  
  def remove_accent(self, word):
    return unidecode.unidecode(word)
  
  def __detach_kb_case(self, word):
    words = re.split(self.KB_CASE_EXP, word)
    return list(filter(None, words))

  def __detach_cp_case(self, word):
    return re.findall(self.CP_CASE_EXP, word)

  def detach(self, source_word):
    words = self.__detach_kb_case(source_word)
    detached_words = map(self.__detach_cp_case, words)
    detached_words = [item for sublist in detached_words for item in sublist]
    
    return detached_words

  def stem(self, word):
    if not hasattr(self, 'stemmer'):
      return word
    
    return self.stemmer.stem(word)
