from question_builder.data import DataQuestion
from . import pos_validators
from ..questions.question import Question, N_BAITS
from .question_creator import QuestionCreator
from ..dictionary_factory import word2meanslike, CORRECT, BAITS
from .question_creator_exception import WordNotNoun, WordNotInMeansLikeDictionary
import random

class MeansLikeQuestionCreator(QuestionCreator):

    code = "ML"
    baits_code = "notml"

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
        question.correct_answer = self._get_correct_answer(pos, target_lemma)
        question.baits = self._get_baits(target_lemma)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos, target_word):
        if not pos_validators.is_noun(pos):
            raise WordNotNoun()
        if target_word not in word2meanslike:
            raise WordNotInMeansLikeDictionary()
        return word2meanslike[target_word][CORRECT]

    def _get_phrase(self, original_phrase, target_word):
        return self._underline_word(original_phrase, target_word)

    def _get_baits(self, target_word):
        return random.sample(word2meanslike[target_word][BAITS], N_BAITS)