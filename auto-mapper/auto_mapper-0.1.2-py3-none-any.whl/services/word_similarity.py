import requests

from mapper.utils.common import Singleton

class WordSimilarity(metaclass=Singleton):
  """
  Word Similarity Service
  """
  __BASE_URL = 'https://api.datamuse.com/words'
  __WIKI_VOCABULARY = 'enwiki'
  __MAX = 1000


  def find_similar(self, text, use_wiki=False, max = 100):
    """
    A list of words with similar meaning to the text
    """
    
    params = {'ml': text}
    if use_wiki:
      params.update({'v': self.__WIKI_VOCABULARY})
    if max > self.__MAX:
      max = self.__MAX
    
    params.update({'max': max})
    
    r = requests.get(self.__BASE_URL, params=params)

    similar_words = []

    if r.status_code == requests.codes.ok:
      similar_words = r.json()

    extracted_words = map(lambda elm: elm['word'], similar_words)
    
    return list(extracted_words)

