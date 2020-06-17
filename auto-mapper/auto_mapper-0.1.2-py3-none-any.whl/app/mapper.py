from mapper.app.text_cleaner import TextCleaner
from mapper.services.word_similarity import WordSimilarity
from mapper.utils.word_utils import word2vec, cosine_similarity
from mapper.utils.common import is_iterable

from itertools import product
from statistics import mean
import json

class Mapper:
  WORD_THRESHOLD = 0.9 # threshold to consider 2 words similar
  VECTOR_THRESHOLD_01 = 0.7 # threshold to consider 2 word vectors similar
  VECTOR_THRESHOLD_02 = 0.577 # threshold to consider 2 word vectors similar


  def __init__(self):
    self.txtCln = TextCleaner(stemming=True)

  def __init_mapping(self, column_names = [], fields = []):
    """
    Initialize essential structures for the mapping operation
    """
    self.word_similarity_service = WordSimilarity()
    self.unmapped_columns = set(range(0, len(column_names)))
    self.unmapped_fields = set(range(0, len(fields)))
    self.mapping_result = set()

  def __clean_field(self, field):
    return self.txtCln.clean(field['name'])

  def __clean_element(self, element):
    return self.txtCln.clean(element)

  def __stem_elements(self, elements, to_stem):
    """
    Apply stemming on each element

    elements: 2D list
    to_stem: indices of elements to stem
    """

    stem_element_value = lambda elm: (elm[0], self.txtCln.stem_tokens(elm[1]))

    elements_to_stem = map(lambda i: elements[i], to_stem)
    stemmed_elements = map(stem_element_value, elements_to_stem)

    return list(stemmed_elements)

  def __tokenize_elements(self, elements, consumer):
    """
    Preprocess elements and generate a list of tokens for each element

    elements: list to be tokenized
    consumer: extractor function (in case elements is a list of object we must specify what property to tokenize)
    """
    tokenized_elements = map(consumer, elements)

    return list(tokenized_elements)

  def __vectorize_element(self, element):
    """
    Convert the element to the corresponding vector.
    
    element: single string or a 1D list of strings
    """

    return word2vec(element)
  
  def __vectorize_elements(self, elements = []):
    """
    Convert each element from the list to the corresponding vector.
    
    elements: 1D or 2D list of words
    """
    vectorized_elements = [self.__vectorize_element(element) for element in elements]

    return vectorized_elements

  def __vectorize_tokens(self, tokenized_elements = [], deep = False):
    """
    Conversion of tokenized_elements to the corresponding vectors.

    tokenized_elements: 2D list of words.
    deep: if true apply the conversion on the nested elements, which results in a 2D list of vectors. Otherwise, generates a 1D list of vectors
    """
    
    if deep == True:
      to_vectorize = lambda elm: (elm[0], self.__vectorize_elements(elm[1]))
    else:
      to_vectorize = lambda elm: (elm[0], self.__vectorize_element(elm[1]))

    vectorized_tokens = map(to_vectorize, tokenized_elements)

    return list(vectorized_tokens)

  def __ignore_multiwords(self, tokenized_elements, to_consider):
    """
    Ignore elements for which the number of tokens is greater than 1
    """

    if not is_iterable(tokenized_elements) or not is_iterable(to_consider):
      raise ValueError("illegal arguments passed")

    unmapped_elements = map(lambda idx: tokenized_elements[idx], to_consider)
    single_words = filter(lambda elm: len(elm[1]) == 1, unmapped_elements)
    single_words = map(lambda elm: (elm[0], elm[1][0]), single_words)

    return list(single_words)

  def __map_to_similar_words(self, tokenized_elements = []):
    """
    Map each token to a set of similar words (words with the same meaning)
    """
    get_similar_words = lambda word: set(self.word_similarity_service.find_similar(word))
    converter = lambda elm: (elm[0], get_similar_words(elm[1]))

    fields_similar_words = map(converter, tokenized_elements)

    return list(fields_similar_words)

  def __common_mapping_phase(self, tokenized_columns, tokenized_fields, threshold):
    """
    Map each element from fields to the most similar column using vector's cosine similarity.

    tokenized_columns: 2D list
    tokenized_fields: 2D list
    threshold: float number
    """

    if not is_iterable(tokenized_columns) or not is_iterable(tokenized_fields) or not isinstance(threshold, float):
      raise ValueError("illegal arguments passed")

    # Vectorize each list of tokens
    vectorized_columns = self.__vectorize_tokens(tokenized_columns)
    vectorized_fields = self.__vectorize_tokens(tokenized_fields)

    for f_idx, v_field in vectorized_fields:
      max_score = 0
      mapped_col = -1
      for c_idx, v_column in vectorized_columns:
        score = cosine_similarity(v_field, v_column)
        if score > max_score and score >= threshold:
          max_score = score
          mapped_col = c_idx
      
      if mapped_col != -1:
        entry = json.dumps({
          'source': mapped_col,
          'target': f_idx,
          'score': max_score
        })
        self.mapping_result.add(entry)

        self.unmapped_columns.discard(mapped_col)
        self.unmapped_fields.discard(f_idx)
  
  def __mapping_phase1(self, tokenized_columns = [], tokenized_fields = []):
    """
    Map each element from fields to the most similar column using vector's cosine similarity.
    """

    # These phase doesn't require any additional cleaning
    self.__common_mapping_phase(tokenized_columns, tokenized_fields, self.VECTOR_THRESHOLD_01)
  
  def __mapping_phase2(self, tokenized_columns = [], tokenized_fields = []):
    """
    Map each element from fields to the most similar column using vector's cosine similarity.
    This phase use an additional cleaning process "stemming" to shrink the mapping interval.
    it's only applied on the unmapped fields
    """

    # Additional cleaning process
    stemmed_columns = self.__stem_elements(tokenized_columns, self.unmapped_columns)
    stemmed_fields = self.__stem_elements(tokenized_fields, self.unmapped_fields)
    
    # Apply the mapping
    self.__common_mapping_phase(stemmed_columns, stemmed_fields, self.VECTOR_THRESHOLD_02)


  def __mapping_phase3(self, tokenized_columns = [], tokenized_fields = []):
    """
    This is a special mapping phase where:
    - multiwords are ignored: it maps single words only
    - each token from fields is converted to a list of similar words using the external API
    """

    unmapped_fields = map(lambda idx: tokenized_fields[idx], self.unmapped_fields)

    single_token_columns = self.__ignore_multiwords(tokenized_columns, self.unmapped_columns)
    single_token_fields = self.__ignore_multiwords(tokenized_fields, self.unmapped_fields)

    fields_similar_words = self.__map_to_similar_words(single_token_fields)

    for c_idx, column_name in single_token_columns:
      for f_idx, field_tokens in fields_similar_words:
        if column_name in field_tokens:
          entry = json.dumps({
            'source': c_idx,
            'target': f_idx,
            'score': 1.0
          })
          self.mapping_result.add(entry)

          self.unmapped_columns.discard(c_idx)
          self.unmapped_fields.discard(f_idx)

  def __generate_mapping_result(self, column_names = [], fields = []):
    """
    Replace indices with concrete value from column_names and fields
    """

    load_mapping_result = map(lambda m: json.loads(m), self.mapping_result)
    mapping_result = map(lambda m: {
      'source': [column_names[m['source']]],
      'target': fields[m['target']]['code']
    }, load_mapping_result)

    return list(mapping_result), self.unmapped_columns, self.unmapped_fields

  def map(self, column_names = [], fields = []):
    """
    Maps column_names to the most similar fields

    column_names: list of strings
    fields: list of objects where each object must have a code a name

    returns:
    mapping_result: list of objects of the format {'source': ['column_name'], 'target': 'field_code'}
    unmapped_columns: set of indices of the unmapped columns
    unmapped_fields: set of indices of the unmapped fields
    """

    self.__init_mapping(column_names, fields)
    
    tokenized_columns = self.__tokenize_elements(column_names, self.__clean_element)
    tokenized_fields =  self.__tokenize_elements(fields, self.__clean_field)

    # Add indices to the structure
    tokenized_columns = list(enumerate(tokenized_columns))
    tokenized_fields = list(enumerate(tokenized_fields))

    self.__mapping_phase1(tokenized_columns, tokenized_fields)
    self.__mapping_phase2(tokenized_columns, tokenized_fields)
    self.__mapping_phase3(tokenized_columns, tokenized_fields)
    
    ## TESTS

    return self.__generate_mapping_result(column_names, fields)
    