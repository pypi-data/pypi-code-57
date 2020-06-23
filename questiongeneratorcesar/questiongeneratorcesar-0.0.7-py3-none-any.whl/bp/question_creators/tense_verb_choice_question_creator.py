from question_builder.data import DataQuestion
from . import pos_validators
from ..questions.question import Question
from .question_creator import QuestionCreator
from .question_creator_exception import NoLexemasFound, WordNotVerb
import random
import editdistance

class TenseVerbChoiceQuestionCreator(QuestionCreator):
    code = "TVC"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        pos = data_question.pos
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(
            content)
        question.correct_answer = target_word
        question.baits = self._get_baits(target_word, pos)
        question.options = self._get_options(question.correct_answer,
                                             question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _choose_bait(self, possible_baits, target_lemma):
        distances = {}
        for bait in possible_baits:
            distances[bait] = editdistance.eval(target_lemma, bait)
        baits = [bait for bait, distance in distances.items()
                 if distance == min(list(distances.values()))]
        bait = random.choice(baits)
        return [bait]

    def _get_baits(self, target_lemma, pos):
        if not pos_validators.is_verb(pos):
            raise WordNotVerb()
        possible_baits = self.content_repository.get_lexemas_from_lemma(
            target_lemma)
        if not possible_baits:
            raise NoLexemasFound()
        bait = self._choose_bait(possible_baits, target_lemma)
        return bait

    def _get_phrase(self, original_phrase, target_word):
        return self._remove_word(original_phrase, target_word)
