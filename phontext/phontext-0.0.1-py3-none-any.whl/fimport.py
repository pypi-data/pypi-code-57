# Written by Rolando Muñoz (2019-2020)

class WordList(list):
  def __init__(self):
    self.wordList = list()
    
  def get_from_raw_text_file(self, fpath, unique = False):
    wordList = list() 
    with open(fpath, mode = 'r') as f:
      text = f.readlines()
      for line in text:
        word = line.rstrip()
        wordList.append(word)
    if unique:
      wordList = list(set(wordList))
    return wordList.copy()

if __name__ == '__main__':
  fpath = "/home/rolando/Documents/nomatsigenga/trabajo_de_campo_2016/wordList.txt"
  wordList = WordList()
  wordList = wordList.get_from_raw_text_file(fpath, unique = True)
  print(wordList)
