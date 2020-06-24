from question_builder.data import DataQuestion
from ..questions.question import Question
from .question_creator import QuestionCreator
from ..dictionary_factory import word2englishdefinitions
from .question_creator_exception import WordNotInEnglishDefinitionsDictionary
import random

class ChoiceEnglishDefinitionsQuestionCreator(QuestionCreator):

    code = "CED"
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
        question.correct_answer = self._get_correct_answer(target_lemma, pos)
        question.baits = self._get_baits(target_lemma)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, target_lemma, pos):
        if (target_lemma, pos) in word2englishdefinitions:
            return random.choice(word2englishdefinitions[(target_lemma, pos)])
        raise WordNotInEnglishDefinitionsDictionary()

    def _get_baits(self, target_lemma):
        bait = None
        while(True):
            bait = random.choice(list(word2englishdefinitions.keys()))
            if(bait != target_lemma):
                break
        return [random.choice(word2englishdefinitions[bait])]

    def _get_phrase(self, original_phrase, target_word):
        return self._underline_word(original_phrase, target_word)
