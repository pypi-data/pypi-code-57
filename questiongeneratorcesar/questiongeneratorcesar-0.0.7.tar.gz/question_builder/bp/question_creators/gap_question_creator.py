from question_builder.data import DataQuestion
from ..questions.question import Question, N_BAITS
from .question_creator import QuestionCreator
from ..dictionary_factory import word2soundslike
from ..dictionary_factory import pos2words
from .question_creator_exception import WordNotInSoundsLikeDictionary
import random

class GapQuestionCreator(QuestionCreator):

    code = "GAP"
    baits_sounds_code = "sounds"
    baits_pos_code = "pos"

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
        question.correct_answer = target_word
        baits_code, question.baits = self._get_baits(target_word, pos)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = baits_code
        return question


    def _get_baits(self, target_word, pos):
        if target_word in word2soundslike:
            return self.baits_sounds_code, random.sample(word2soundslike[target_word], N_BAITS)  
        else:
            return self.baits_pos_code, random.sample(pos2words[pos], N_BAITS) 

    def _get_phrase(self, original_phrase, target_word):
        return self._remove_word(original_phrase, target_word)
