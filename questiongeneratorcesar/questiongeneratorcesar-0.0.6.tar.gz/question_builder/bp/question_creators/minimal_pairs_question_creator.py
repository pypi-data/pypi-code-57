from question_builder.data import DataQuestion
from ..questions.dual_video_question import DualVideoQuestion
from .question_creator import QuestionCreator
from ..dictionary_factory import word2minimalpair
from .dual_video_question_creator import DualVideoQuestionCreator
from .question_creator_exception import MinimalPairNotFoundException, ContentNotFoundException
import random

class MinimalPairsQuestionCreator(DualVideoQuestionCreator):

    code = "MP"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id):
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        incorrect_content = self._get_bait_content(target_lemma, user_id)
        correct_content = data_question.content
        question = DualVideoQuestion()
        question.content_id = correct_content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        medias_list = self._get_medias([correct_content, incorrect_content])
        question.links = medias_list.links
        question.media_types = medias_list.media_types
        question.phrases = medias_list.phrases
        question.correct_values = medias_list.correct_values
        question.options = None
        question.phrase = self._get_phrase(correct_content)
        question.phrase_translation = self._get_translation(correct_content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_bait_content(self, target_lemma, user_id):
        if target_lemma in word2minimalpair:
            pairs = word2minimalpair[target_lemma]
            content = self.content_repository.get_question(user_id, pairs)
            if(content):
                return content.content
            raise ContentNotFoundException()
        raise MinimalPairNotFoundException()

    def _get_phrase(self, content):
        return content.phrase

    def _get_translation(self, content):
        if hasattr(content, 'translation'):
            if content.translation is not None:
                phrase_translation = content.translation.strip()
            else:
                phrase_translation = ""
        else:
            phrase_translation = ""
        return phrase_translation

