from collections import Counter
from functools import reduce

import math
import operator

# Constants
NUMBER_OF_DIGITS = 8

# Methods
def to_counter(word_or_list):
  """
  Generates a word/list counter: map the number of occurrences to each distinct character/word
  """
  return Counter(word_or_list)

def set_of_distinct(word_or_list_counter):
  """
  Generates a set of distinct characters/words

  word_or_list_counter: Counter of the original word/list
  """

  if not isinstance(word_or_list_counter, Counter):
    raise ValueError("word_or_list_counter must be a counter")

  return set(word_or_list_counter)
  
def length(word_or_list_counter):
  """
  Calculate the length of a word/list
  the length of a given word/list is defined as:
    l = sqrt( sum(ci*ci) ) where ci is the number of occurrences of i-th character/word

  word_or_list_counter: Counter of the original word/list
  """

  if not isinstance(word_or_list_counter, Counter):
    raise ValueError("word_or_list_counter must be a counter")

  values = map(lambda ci: ci*ci, word_or_list_counter.values())
  magnitude = reduce(operator.add, values)

  return math.sqrt(magnitude)

def word2vec(word_or_list):
  """
    Convert a word/list to vector of the format: [word_or_list_counter, distinct_elements, word_or_list_length]
  """

  word_or_list_counter = to_counter(word_or_list)
  distinct_elements = set_of_distinct(word_or_list_counter)
  word_or_list_length = length(word_or_list_counter)

  return [word_or_list_counter, distinct_elements, word_or_list_length]

def cosine_similarity(vector_1, vector_2):
  """
  Calculate cosine similarity between 2 word-or-list-vectors
  The equation is defined as:
  similarity = cos(theta) = sum(Ai * Bi)/(length(A) * length(B)) where:
  - A and B are 2 words/lists
  - Ai and Bi are the number of occurrences of character/word i
  - i (0..n) is the i-th common character/word between A and B
  """
    
  # Get the common characters/words between A and B
  common_elements = vector_1[1].intersection(vector_2[1])

  # Sum of the product of each intersection.
  product = map(lambda c_char: vector_1[0][c_char] * vector_2[0][c_char], common_elements)
  product_summation = reduce(operator.add, product, 0)

  length = vector_1[2] * vector_2[2]

  # Calculates cosine similarity and rounds the value to NUMBER_OF_DIGITS decimal places.
  if length == 0: # empty word
    similarity = 0
  else:
    similarity = round(product_summation/length, NUMBER_OF_DIGITS)
  
  return similarity