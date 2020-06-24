from question_builder.data import DataQuestion
from . import pos_validators
from ..questions.question import Question, CORRECT, TEXT, N_BAITS
from .question_creator import QuestionCreator
from ..dictionary_factory import word2presuffix, CORRECT as DICT_CORRECT, BAITS
from .question_creator_exception import WordHasNotValidPos, WordNotInPreSuffixDictionary
import random
import re

class SubwordQuestionCreator(QuestionCreator):

    code = "SWS"
    baits_code = "nopreffixsuffix"

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
        question.correct_answer = self._get_correct_answer(pos, target_word)
        question.baits = self._get_baits(target_word)
        question.options = self._get_options(question.correct_answer, question.baits, target_word)
        question.phrase = self._get_phrase(content.phrase, target_word, question.correct_answer)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos, target_word):
        valid_pos = pos_validators.is_noun(pos) or \
                    pos_validators.is_verb(pos) or \
                    pos_validators.is_adverb(pos)
        if(not valid_pos):
            raise WordHasNotValidPos()
        if(target_word not in word2presuffix):
            raise WordNotInPreSuffixDictionary()
        return word2presuffix[target_word][DICT_CORRECT]

    def _get_options(self, correct_answer, baits, target_word):
        """
        Get the baits and the words, and make an array of Options Objects in
        which word is set to True, and all others are False
        """
        is_prefix = target_word.startswith(correct_answer)
        options = [{TEXT: self._add_line_to_option(correct_answer, is_prefix),
                    CORRECT: True}]
        for bait in baits:
            options.append({TEXT: self._add_line_to_option(bait, is_prefix),
                           CORRECT: False})
        random.shuffle(options)
        return options

    def _get_phrase(self, original_phrase, target_word, correct_answer):
        return self._remove_word(original_phrase, 
                                target_word, 
                                correct_answer)

    def _get_baits(self, target_word):
        return random.sample(word2presuffix[target_word][BAITS], N_BAITS)

    def _add_line_to_option(self, option, is_prefix):
        if(is_prefix):
            return option + "-"
        else:
            return "-" + option

    def _remove_word(self, phrase, target_word, correct_answer):
        is_prefix = target_word.startswith(correct_answer)
        substitution = target_word.replace(correct_answer,
                                           self._add_space_to_dash(is_prefix),
                                           1)
        phrase = re.sub(r"\b" + target_word + r"(\b|(?=n't))",
                        substitution, phrase, flags=re.I, count=1)
        phrase = self._clean_phrase(phrase)
        phrase = self._underline_word(phrase, substitution)
        return phrase

    def _add_space_to_dash(self, is_prefix):
        if(is_prefix):
            return "    -"
        else:
            return "-    "