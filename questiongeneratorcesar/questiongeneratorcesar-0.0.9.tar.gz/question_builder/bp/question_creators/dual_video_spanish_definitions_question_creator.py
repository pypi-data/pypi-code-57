from question_builder.data import DataQuestion
from ..questions.question import Question, N_BAITS
from .pos_validators import NOUN, VERB, ADJ, ADV
from ..questions.dual_video_question import DualVideoQuestion
from .dual_video_question_creator import DualVideoQuestionCreator
from .dual_video_question_creator import PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO
from ..dictionary_factory import word2spanishdefinitions
from .question_creator_exception import DefinitionNotFoundException
from .question_creator_exception import ContentNotFoundException
from .question_creator_exception import SpanishBaitsNotFoundException
import random

class DualVideoSpanishDefinitionsQuestionCreator(DualVideoQuestionCreator):

    code = "DVS"
    baits_code = "nobaits"
    
    def create(self, data_question: DataQuestion, user_id):
        
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        incorrect_content = self._get_bait_content(target_lemma, user_id)
        correct_content = data_question.content
        definition = self._get_definition(target_lemma)

        question = DualVideoQuestion()
        question.content_id = correct_content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        medias_list = self._get_medias([correct_content, incorrect_content])
        question.links = medias_list.links
        question.media_types = medias_list.media_types
        question.phrases = medias_list.phrases
        question.correct_values = medias_list.correct_values
        question.definition = definition
        question.options = None
        question.phrase = definition
        question.phrase_translation = ""
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_definition(self, target_lemma):
        
        if((target_lemma, NOUN) in word2spanishdefinitions):
            key = (target_lemma, NOUN)
        elif((target_lemma, VERB) in word2spanishdefinitions):
            key = (target_lemma, VERB)
        elif((target_lemma, ADV) in word2spanishdefinitions):
            key = (target_lemma, ADV)
        elif((target_lemma, ADJ) in word2spanishdefinitions):
            key = (target_lemma, ADJ)
        else:
            raise DefinitionNotFoundException()

        return word2spanishdefinitions[key][0]

    def _get_bait_content(self, target_lemma, user_id):
        baits = random.sample(list(word2spanishdefinitions.keys()), N_BAITS)
        baits = [bait[0] for bait in baits if bait[0] != target_lemma]
        if baits:   
            content = self.content_repository.get_question(user_id, baits)
            if(content):
                return content.content
            raise ContentNotFoundException()
        raise SpanishBaitsNotFoundException()




