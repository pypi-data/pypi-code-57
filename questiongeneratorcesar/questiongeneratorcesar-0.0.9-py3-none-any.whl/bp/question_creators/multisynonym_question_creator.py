from question_builder.data import DataQuestion
from ..questions.question import Question, CORRECT, TEXT
from .question_creator import QuestionCreator
from ..dictionary_factory import word2multisynonym, pos2words
from .question_creator_exception import WordNotInMultiSynonymDictionary
from ...config import MAX_SYNONYM_ANSWERS
import random

class MultiSynonymQuestionCreator(QuestionCreator):

    code = "MSYN"
    baits_code = "pos"

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
        question.baits = self._get_baits(pos, question.correct_answer)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos, target_word):
        if((target_word, pos) in word2multisynonym):
            synonym_list = word2multisynonym[(target_word, pos)]
        elif((target_word, None) in word2multisynonym):
            synonym_list = word2multisynonym[(target_word, None)]
        else:
            raise WordNotInMultiSynonymDictionary()

        if(len(synonym_list) <= MAX_SYNONYM_ANSWERS):
            synonyms = synonym_list[:]
            random.shuffle(synonyms)
        else:
            synonyms = random.sample(synonyms, \
                MAX_SYNONYM_ANSWERS)
        return synonyms

    def _get_phrase(self, original_phrase, target_word):
        return self._underline_word(original_phrase, target_word)

    def _get_baits(self, pos, correct_answer):
        baits = set()
        n_baits = MAX_SYNONYM_ANSWERS - len(correct_answer)
        baits.update(random.sample(pos2words[pos], MAX_SYNONYM_ANSWERS))
        while(len(baits) < n_baits):
            rnd_pos = random.choice(list(pos2words.keys()))
            if(rnd_pos != pos):
                baits.update(pos2words[rnd_pos])
        return list(baits)[:n_baits]

    def _get_options(self, correct_answer, baits):
        """
        Get the baits and the words, and make an array of Options Objects in
        which word is set to True, and all others are False
        """
        options = []
        for word in correct_answer:
            options.append({TEXT: word, CORRECT: True})
        for bait in baits:
            options.append({TEXT: bait, CORRECT: False})
        random.shuffle(options)
        return options