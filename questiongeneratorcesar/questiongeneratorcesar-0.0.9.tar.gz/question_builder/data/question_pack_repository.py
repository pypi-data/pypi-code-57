from collections import defaultdict
from . import queries


QUESTION_PACK_KEY = "question_pack"
CODE_KEY = "code"
LEVEL_KEY = "level"
QUESTION_TYPES_KEY = "question_types"
ENABLED_KEY = "enabled"

class QuestionPackRepository():
    """
    Handles all the db operations related to question pack management
    """
    def __init__(self, driver):
        """
        Initializes the neo4j db
        """
        self._driver = driver

    def get_question_packs(self):
        question_packs = {}
        with self._driver.session() as session:
            for res in session.read_transaction(self._get_question_packs):
                question_pack_code = res[QUESTION_PACK_KEY][CODE_KEY]
                level = res[LEVEL_KEY]
                for question_type in res[QUESTION_TYPES_KEY]:
                    if question_pack_code not in question_packs:
                        question_packs[question_pack_code] = defaultdict(list)
                    if question_type[ENABLED_KEY]:
                        question_packs[question_pack_code][level].append(
                            question_type[CODE_KEY])
        return question_packs

    @staticmethod
    def _get_question_packs(tx):
        query = queries.GET_QUESTION_PACKS
        results = tx.run(query)
        return results
