from nltk.tokenize import word_tokenize
from mapper.app.word_transformation import WordTransformation
from mapper.utils.common import deprecated

class TextCleaner:

  def __init__(self, stop_word_removal = False, stemming = False, lang='english'):
    self.wordTns = WordTransformation(stop_word=stop_word_removal, use_stemmer=stemming, lang=lang)

  def tokenize(self, source):
    return word_tokenize(source)

  def __lower(self, tokens):
    lowerTokens = map(self.wordTns.lower, tokens)
    return list(lowerTokens)

  def lower(self, source):
    tokens = self.tokenize(source)
    return self.__lower(tokens)
  
  def lower_tokens(self, tokens = []):
    if not isinstance(tokens, list):
      raise ValueError("tokens must be a list")

    return self.__lower(tokens)

  def trim(self, source):
    tokens = self.tokenize(source)
    return " ".join(tokens)

  def __remove_stop_words(self, tokens):
    predicate = lambda token: not self.wordTns.is_stop_word(token)

    filteredList = filter(predicate, tokens)
    return list(filteredList)

  @deprecated("This method is deprecated, it'll be removed in the next release")
  def cut_stop_words(self, source):
    tokens = self.tokenize(source)
    tokens_without_stop_words = self.__remove_stop_words(tokens)
    
    return tokens_without_stop_words

  def __remove_punctuation(self, tokens):
    rp = lambda x: self.wordTns.remove_punctuation(x)

    filteredList = filter(None, map(rp, tokens))
    
    return list(filteredList)

  def cut_punctuation(self, source):
    tokens = self.tokenize(source)
    tokens_without_punctuation = self.__remove_punctuation(tokens)
    
    return tokens_without_punctuation
  
  def cut_tokens_punctuation(self, tokens = []):
    if not isinstance(tokens, list):
      raise ValueError("tokens must be a list")

    tokens_without_punctuation = self.__remove_punctuation(tokens)    
    return tokens_without_punctuation

  def __remove_accent(self, tokens):
    ra = lambda x: self.wordTns.remove_accent(x)
    tokens_without_accent = [ra(token) for token in tokens]

    return tokens_without_accent

  def cut_accent(self, source):
    tokens = self.tokenize(source)
    tokens_without_accent = self.__remove_accent(tokens)
    
    return tokens_without_accent
  
  def cut_tokens_accent(self, tokens = []):
    if not isinstance(tokens, list):
      raise ValueError("tokens must be a list")

    tokens_without_accent = self.__remove_accent(tokens)    
    return tokens_without_accent

  def __detach_tokens(self, tokens):
    detached_tokens = map(self.wordTns.detach, tokens)
    detached_words = [item for sublist in detached_tokens for item in sublist]

    return detached_words

  def detached(self, source):
    tokens = self.tokenize(source)
    detached_tokens = self.__detach_tokens(tokens)
    
    return detached_tokens
  
  def flatten_tokens(self, tokens = []):
    if not isinstance(tokens, list):
      raise ValueError("tokens must be a list")

    detached_tokens = self.__detach_tokens(tokens)    
    return detached_tokens

  def __stem_tokens(self, tokens):
    stemmed_tokens = map(self.wordTns.stem, tokens)

    return list(stemmed_tokens)

  def stem(self, source):
    tokens = self.tokenize(source)
    stemmed_tokens = self.__stem_tokens(tokens)

    return stemmed_tokens
  
  def stem_tokens(self, tokens = []):
    if not isinstance(tokens, list):
      raise ValueError("tokens must be a list")
    
    stemmed_tokens = self.__stem_tokens(tokens)
    return stemmed_tokens

  def __clean_v1(self, source):
    """
    Apply each transformation separately.
    After tokenization, apply the first transformation on the first generated list.
    Then apply the next transformation on the result of the previous transformation.
    And so on
    """
    tokens = self.tokenize(source)
    tokens = self.__detach_tokens(tokens)
    tokens = self.__remove_punctuation(tokens)
    tokens = self.__lower(tokens)
    tokens = self.__remove_accent(tokens)

    return tokens

  # TODO  
  def __clean_v2(self, source):
    """
    Apply all the transformations on every element of the tokens.
    This way we shrink the amount of iterations.
    """
    return []

  def clean(self, source):
    """
    Apply a predefined cleaning pipeline on the given text without stemming
    The pipeline is defined as:
      - tokenization
      - detach
      - remove punctuation
      - lowercase
      - remove accent
    """
    return self.__clean_v1(source)
    
  
  def stemmed_clean(self, source):
    """
    Apply the clean pipeline with stemming
    The pipeline is defined as:
      - default clean pipeline
      - stemming
    """
    tokens = self.clean(source)
    tokens = self.__stem_tokens(tokens)

    return tokens