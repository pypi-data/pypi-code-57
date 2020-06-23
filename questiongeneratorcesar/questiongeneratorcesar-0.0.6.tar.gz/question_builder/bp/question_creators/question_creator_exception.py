class QuestionCreatorException(Exception):
    pass

#  Pos exceptions


class WordNotAdjective(QuestionCreatorException):
    pass


class WordNotVerb(QuestionCreatorException):
    pass


class NotConjugation(QuestionCreatorException):
    pass


class InvalidMorpheme(QuestionCreatorException):
    pass


class WordNotNoun(QuestionCreatorException):
    pass

#  Not in dictionary exceptions


class WordNotInAntonymDictionary(QuestionCreatorException):
    pass


class WordNotInEnglishDefinitionsDictionary(QuestionCreatorException):
    pass


class WordNotInSpanishDefinitionsDictionary(QuestionCreatorException):
    pass


class WordNotInSoundsLikeDictionary(QuestionCreatorException):
    pass


class WordNotInIntruderDictionary(QuestionCreatorException):
    pass


class WordNotInMeansLikeDictionary(QuestionCreatorException):
    pass


class WordNotInMultiSynonymDictionary(QuestionCreatorException):
    pass


class WordNotInPartWordTypingDictionary(QuestionCreatorException):
    pass


class WordNotInRelNounDictionary(QuestionCreatorException):
    pass


class WordNotInPreSuffixDictionary(QuestionCreatorException):
    pass


class WordNotInMultisynonymDictionary(QuestionCreatorException):
    pass


class WordNotInSoundsLikeDictionary(QuestionCreatorException):
    pass

#  Dual video exceptions


class DefinitionNotFoundException(QuestionCreatorException):
    pass


class BaitNotFoundException(QuestionCreatorException):
    pass


class MinimalPairNotFoundException(QuestionCreatorException):
    pass


class SpanishBaitsNotFoundException(QuestionCreatorException):
    pass


class ContentNotFoundException(QuestionCreatorException):
    pass


class MaximumLengthExceeded(QuestionCreatorException):
    pass


class WordHasNotValidPos(QuestionCreatorException):
    pass

# other exceptions


class NoLexemasFound(QuestionCreatorException):
    pass
