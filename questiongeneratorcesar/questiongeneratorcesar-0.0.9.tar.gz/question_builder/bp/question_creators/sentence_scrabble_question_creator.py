from question_builder.data import DataQuestion
from ...config import MIN_SENTENCE_SCRABBLE_LENGTH, MAX_SENTENCE_SCRABBLE_LENGTH
from ..questions.question import Question, TEXT, CORRECT
from .question_creator import QuestionCreator
from .question_creator_exception import MaximumLengthExceeded
import re

class SentenceScrabbleQuestionCreator(QuestionCreator):

    code = "SESB"
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
        question.correct_answer = self._get_correct_answer(content.phrase)
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, original_phrase):
        length = len(original_phrase.split())
        if  MIN_SENTENCE_SCRABBLE_LENGTH < length < MAX_SENTENCE_SCRABBLE_LENGTH:
            return [token for token in original_phrase.split()[1:-1] if len(token)> 0]
        raise MaximumLengthExceeded()

    def _get_baits(self):
        return []

    def _get_options(self, correct_answer, baits):
        """
        Get the baits and the words, and make an array of Options Objects in
        which word is set to True, and all others are False
        """
        options = []
        for answer in correct_answer:
            options.append({TEXT: answer, CORRECT: True})
        for bait in baits:
            options.append({TEXT: bait, CORRECT: False})
        return options

    def _get_phrase(self, original_phrase):
        return self._remove_words(original_phrase)

    def _remove_words(self, original_phrase):
        complete_phrase = original_phrase.split()
        inner_phrase = re.sub(r"[^ ]", r'_', " ".join(complete_phrase[1:-1]), flags=re.I)
        phrase = " ".join([complete_phrase[0], inner_phrase, complete_phrase[-1]])
        phrase = self._clean_phrase(phrase)
        return phrase