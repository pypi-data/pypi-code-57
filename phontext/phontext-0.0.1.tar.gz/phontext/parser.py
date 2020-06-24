# Written by Rolando Muñoz (2019-2020)

class PhonParser:
  def __init__(self):
    self.complexCharList = []
  
  def set_complex_chars(self, complexCharList):
    complexCharList = sorted(complexCharList, key=len, reverse = True)
    self.complexCharList = complexCharList
    
  def to_word(self, word):
    """ Split segments from a word
    Parameters:
    word (string): a word to be segmented
    Returns:
    Word: a segment representation of a word 
    """
    lst_word = list()
    while word != '':
      charLen = self.__char_distance(word)
      phon = word[0:charLen]
      word = word[charLen:]
      lst_word.append(phon)
    return Word(lst_word)
    
  def __char_distance(self, word):
    """ Calculate how many characters should count as one segment from the start of a word 
    Parameters:
    word (string): a word to be segmented
    Returns:
    int: the number of characters that count as one segment at the start of a word
    """
    charLen = 1
    for char in self.complexCharList:
      if word.startswith(char):
        charLen = len(char)
        break
    return charLen

class Word():
  def __init__(self, lst_word):
    self.word = lst_word
  
  def __str__(self):
    return ' '.join(self.word)
  
  def __len__(self):
    return self.word.__len__()
  
  def __iter__(self):
    return self.word.__iter__()

  def __reversed__(self):
    return self.word.__reversed__()
    
  def __getitem__(self, index):
    return self.word.__getitem__(index)
  
  def __contains__(self, char):
    return self.word.__contains__(char)
    
  def __eq__(self, other):
    return self.word.__eq__(other.word)

  def __ne__(self, other):
    return self.word.__ne__(other.word)
  
  def __setitem__(self, index, value):
    return self.word.__setitem__(index, value)
    
  def startswith(self, segment):
    return self[0] == segment
  
  def endswith(self, segment):
    maxIndex = len(self) - 1
    return self[maxIndex] == segment
    
  def copy(self):
    return Word(self.word.copy())
  
  def reverse(self):
    self.word = [element for element in self.__reversed__()]
    
  def is_minimaldiff(self, other):
    """ Check if there is a minimal pair with other word object
    It does not take in care if the difference is between a consonant and a vowel (eg. cana vs cant).
    Parameters:
    other (Word): A segment representation of a word
    Returns:
    boolean: True or False
    """
    if not len(self) == len(other):
      return False

    if self == other:
      return False

    diffCounter = 0
    for i in range(0, len(self)):
      if self[i] != other[i]:
        diffCounter+=1
        
      if diffCounter > 1:
        return False
    return True
  
  def to_cv(self, nucleusList = ['a', 'e', 'i', 'o', 'u']):
    """ Convert to CV
    Parameters:
    nucleusList (list): a list of syllabic nuclei
    Returns:
    str: a cv representation of a word 
    """    
    cvPattern = list()
    for phon in self:
      if phon in nucleusList:
        cvPattern.append('V')
      else:
        cvPattern.append('C')
    cvPattern= ''.join(cvPattern)
    return cvPattern

  def get_invalid_segments(self, validSegmentList = []):
    """ Get a list of invalid segments in a word
    Parameters:
    validSegmentList (list): a list of valid segment strings
    Returns:
    list: only invalid segments 
    """   
    return [phon for phon in self if not phon in validSegmentList]
    
if __name__ == '__main__':
  parser = PhonParser()
  parser.set_complex_chars(['ch', 'ts', 'aa'])
  word1 = parser.to_word('chincha')
  word2 = parser.to_word('chinchaa')
  print(word1)
