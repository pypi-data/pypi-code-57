"""
    Occurrence module is composed only by the Occurrence class.
"""
from matchup.presentation.text import Term


class Occurrence:
    """
        Occurrence is an encapsulation of:
            document name, keyword, frequency of term in document, positions and score
        Occurrence is an data structure used to compose Vocabulary.
    """
    def __init__(self, doc: str = "", term: Term = None):
        """
            Occurrence constructor.
        :param doc: String that represents the document name
        :param term: Term that encapsulate the keyword and its position in document.
        """
        self._doc = doc
        self._keyword = term.word if term is not None else None
        self._score = 0

        self._frequency = 1
        self._positions = [term.position] if term is not None else []

    def __str__(self) -> str:
        """
        :return: String representation of an Occurrence
        """
        return "('{0}', '{1}', {2}, {3})".format(self._doc, self._keyword, self._frequency, self._positions)

    def __repr__(self) -> str:
        """
        :return: Return the String representation
        """
        return str(self)

    def __eq__(self, doc: str) -> bool:
        """
            Overload the equal operator by document
        :param doc: String that represents the document file name
        :return: boolean flag that indicates if the both documents are equal
        """
        return self._doc == doc

    def add(self, *, position: str = None) -> None:
        """
            Push this occurrence position in doc for the Occurrence structure
        :param position: String that represents the position. Ex : '1-19'
        :return: None
        """
        if position is not None:
            self._positions.append(position)
        self._frequency += 1

    def doc(self) -> str:
        """
            Property that return the document name
        :return: document string name
        """
        return self._doc

    @property
    def frequency(self) -> int:
        """
           Property that return the frequency of term i in document j
        :return: document string name
        """
        return self._frequency

    @property
    def score(self) -> float:
        """
            Property that return the score of this Occurrence
        :return: Score of occurrence
        """
        return self._score

    @score.setter
    def score(self, scr: float) -> None:
        """
            Property setter score
        :param scr: float score
        :return: None
        """
        self._score = scr

    @property
    def keyword(self) -> str:
        """
            Keyword property getter
        :return: Keyword name
        """
        return self._keyword

    @keyword.setter
    def keyword(self, kw: str) -> None:
        """
            Keyword property setter
        :param kw: Keyword to update
        :return: None
        """
        self._keyword = kw
