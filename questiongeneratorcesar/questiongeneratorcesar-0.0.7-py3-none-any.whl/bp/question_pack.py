from .question_creators.antonym_question_creator import AntonymQuestionCreator
from .question_creators.subword_question_creator import SubwordQuestionCreator
from .question_creators.intruder_question_creator import IntruderQuestionCreator
from .question_creators.synonym_question_creator import SynonymQuestionCreator
from .question_creators.means_like_question_creator import MeansLikeQuestionCreator
from .question_creators.relnoun_question_creator import RelNounQuestionCreator
from .question_creators.gap_question_creator import GapQuestionCreator
from .question_creators.minimal_pairs_question_creator import MinimalPairsQuestionCreator
from .question_creators.partword_typing_question_creator import PartWordTypingQuestionCreator
from .question_creators.dual_video_spanish_definitions_question_creator import DualVideoSpanishDefinitionsQuestionCreator
from .question_creators.choice_spanish_definitions_question_creator import ChoiceSpanishDefinitionsQuestionCreator
from .question_creators.multisynonym_question_creator import MultiSynonymQuestionCreator
from .question_creators.intruder_question_creator import IntruderQuestionCreator
from .question_creators.choice_english_definitions_question_creator import ChoiceEnglishDefinitionsQuestionCreator
from .question_creators.fullword_scrabble_question_creator import FullWordScrabbleQuestionCreator
from .question_creators.sentence_scrabble_question_creator import SentenceScrabbleQuestionCreator
from .question_creators.fullword_typing_question_creator import FullWordTypingQuestionCreator
from .question_creators.conjugation_question_creator import ConjugationQuestionCreator
from .question_creators.tense_verb_choice_question_creator import TenseVerbChoiceQuestionCreator

QUESTION_PACK_TEST_CODE = "GMPT"
QUESTION_PACK_ALL_CODE = "GMPALL"

question_type_to_creator = {
    GapQuestionCreator.code: GapQuestionCreator,
    MinimalPairsQuestionCreator.code: MinimalPairsQuestionCreator,
    SubwordQuestionCreator.code: SubwordQuestionCreator,
    PartWordTypingQuestionCreator.code: PartWordTypingQuestionCreator,
    DualVideoSpanishDefinitionsQuestionCreator.code: DualVideoSpanishDefinitionsQuestionCreator,
    ChoiceSpanishDefinitionsQuestionCreator.code: ChoiceSpanishDefinitionsQuestionCreator,
    SynonymQuestionCreator.code: SynonymQuestionCreator,
    AntonymQuestionCreator.code: AntonymQuestionCreator,
    MeansLikeQuestionCreator.code: MeansLikeQuestionCreator,
    RelNounQuestionCreator.code: RelNounQuestionCreator,
    MultiSynonymQuestionCreator.code: MultiSynonymQuestionCreator,
    IntruderQuestionCreator.code: IntruderQuestionCreator,
    ChoiceEnglishDefinitionsQuestionCreator.code: ChoiceEnglishDefinitionsQuestionCreator,
    FullWordScrabbleQuestionCreator.code: FullWordScrabbleQuestionCreator,
    SentenceScrabbleQuestionCreator.code: SentenceScrabbleQuestionCreator,
    FullWordTypingQuestionCreator.code: FullWordTypingQuestionCreator,
    ConjugationQuestionCreator.code: ConjugationQuestionCreator,
    TenseVerbChoiceQuestionCreator.code: TenseVerbChoiceQuestionCreator
}


class CreatorNode():
    def __init__(self, question_creator):
        self.question_creator = question_creator
        self.next = None


class QuestionPack():
    def __init__(self, code, level_to_question_types, level_to_master=None):
        self.code = code
        self.level_to_question_types = level_to_question_types
        self.level_to_master = len(level_to_question_types.keys())
        self._question_types = None
        self._question_type_to_level = None
        self._responsibility_chain = None

    @property
    def question_types(self):
        if(self._question_types is None):
            self._question_types = []
            for level, question_types in self.level_to_question_types.items():
                for question_type in question_types:
                    self._question_types.append(question_type)
        return self._question_types

    @property
    def question_type_to_level(self):
        if(self._question_type_to_level is None):
            self._question_type_to_level = {}
            for level, question_types in self.level_to_question_types.items():
                for question_type in question_types:
                    self._question_type_to_level[question_type] = level
        return self._question_type_to_level

    @property
    def responsibility_chain(self):
        """
        Create the responsability chain according to the question pack given
        in the constructor. The chain is a single linked list.
        """
        if(self._responsibility_chain is None):
            self._responsibility_chain = {}
            levels = sorted(
                list(self.level_to_question_types.keys()), reverse=True
            )
            last = None
            for level in levels:
                questions = self.level_to_question_types[level]
                for index in range(len(questions)):
                    #  Get the current node in the chain
                    question_code = questions[index]
                    question_creator = question_type_to_creator[question_code]
                    self._responsibility_chain[question_code] = CreatorNode(
                        question_creator)
                    #  Get the previous node and link it to the current one
                    if(last):
                        last.next = self._responsibility_chain[question_code]
                    last = self._responsibility_chain[question_code]
        return self._responsibility_chain
