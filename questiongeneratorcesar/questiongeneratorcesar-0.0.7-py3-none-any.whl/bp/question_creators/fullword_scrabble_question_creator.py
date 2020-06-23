from question_builder.data import DataQuestion
from ..questions.question import Question
from .question_creator import QuestionCreator

class FullWordScrabbleQuestionCreator(QuestionCreator):

    code = "FWSB"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = target_word
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_baits(self):
        return []

    def _get_phrase(self, original_phrase, target_word):
        return self._remove_word(original_phrase, target_word)
