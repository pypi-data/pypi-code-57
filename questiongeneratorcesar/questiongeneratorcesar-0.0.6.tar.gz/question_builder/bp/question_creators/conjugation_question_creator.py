from question_builder.data import DataQuestion
from . import pos_validators
from ..questions.question import Question
from .question_creator import QuestionCreator
from .question_creator_exception import WordNotVerb, NotConjugation, InvalidMorpheme
import re
import random

MAX_OPTIONS = 10
COMMON_BAITS = "aeioungrmd"

class ConjugationQuestionCreator(QuestionCreator):

    code = "CJG"
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
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(pos, target_word, target_lemma)
        question.baits = self._get_baits(question.correct_answer)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word, question.correct_answer)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos, target_word, target_lemma): 
        if(not pos_validators.is_verb(pos)):
            raise WordNotVerb()
        if(target_word == target_lemma):
            raise NotConjugation()
        morpheme = self._get_morpheme(target_lemma, target_word)
        if(morpheme == target_word):
            raise InvalidMorpheme()
        return morpheme

    def _get_baits(self, correct_answer):
        remaining = MAX_OPTIONS - len(correct_answer)
        baits = self._get_random_baits(remaining)
        return ["".join(baits)]

    def _get_random_baits(self, n):
        return random.sample(COMMON_BAITS, n)

    def _get_phrase(self, original_phrase, target_word, correct_answer):
        return self._remove_word(original_phrase, target_word, correct_answer)
        
    def _remove_word(self, phrase, target_word, correct_answer):
        #speaking, ing
        substitution = re.sub('%s$' % correct_answer, "-    ", target_word)
        phrase = re.sub(r"\b" + target_word + r"(\b|(?=n't))",
                        substitution, phrase, flags=re.I, count=1)
        phrase = self._clean_phrase(phrase)
        phrase = self._underline_word(phrase, substitution)
        return phrase

    def _get_morpheme(self, target_lemma, target_word):
        for i, (char1, char2) in enumerate(zip(target_lemma, target_word)):
            if char1 != char2:
                return target_word[i:]

        return target_word[i+1:]
    