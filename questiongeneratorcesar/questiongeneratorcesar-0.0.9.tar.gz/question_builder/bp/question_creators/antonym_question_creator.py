from question_builder.data import DataQuestion
from . import pos_validators
from ..questions.question import Question, N_BAITS
from .question_creator import QuestionCreator
from ..dictionary_factory import word2antonym, CORRECT, BAITS
from .question_creator_exception import WordNotInAntonymDictionary, WordNotAdjective
import random

class AntonymQuestionCreator(QuestionCreator):

    code = "AN"
    baits_code = "noantonym"
    
    def create(self, data_question: DataQuestion, user_id):
        
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        pos = data_question.pos
        
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(target_word, pos)
        question.baits = self._get_baits(target_word)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, target_word, pos):
        if target_word not in word2antonym:
            raise WordNotInAntonymDictionary()
        if not pos_validators.is_adjective(pos):
            raise WordNotAdjective()
        return word2antonym[target_word][CORRECT][0]
        
    def _get_phrase(self, original_phrase, target_word):
        return self._underline_word(original_phrase, target_word)

    def _get_baits(self, target_word):
        return random.sample(word2antonym[target_word][BAITS], 
                            N_BAITS)

