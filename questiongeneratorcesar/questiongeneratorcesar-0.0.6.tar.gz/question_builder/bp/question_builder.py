from question_builder.data import DataQuestion
from .question_creators.question_creator_exception import QuestionCreatorException  # noqa: E501
import random
import logging


class QuestionBuilder():
    """
    Builds a question given the raw data DataQuestion information.
    It uses the responsibility chain design pattern to find the question
    creator that takes charge of creating the bp question.
    """
    def __init__(self, content_repository):
        self.content_repository = content_repository
        self.question_pack_registry = {}

    def create(self, data_question: DataQuestion, user_id, question_pack_code,
               question_type=None, level=None, mastered=False):
        """
        Creates a question according to the question pack given in the
        arguments
        """
        logging.debug("\nQuestion builder: {} {} {} {} {} {}".format(
            data_question,
            user_id,
            question_pack_code,
            question_type,
            level,
            mastered)
        )
        question_pack = self.question_pack_registry[question_pack_code]
        question_type = self._get_question_type(
            question_type, level, question_pack.question_types,
            question_pack.level_to_question_types
        )
        creator_node = question_pack.responsibility_chain[question_type]
        question_ = self._get_question(creator_node,
                                       data_question,
                                       self.content_repository,
                                       user_id)
        question_.mastered = mastered
        if(level):
            question_.level = level
            question_.level_to_master = question_pack.level_to_master
        return question_

    def _get_question_type(self, question_type, level, default_question_types,
                           default_level_to_question_types):
        """
        Returns the same question type if given in the argument, else return a
        default one
        """
        if(question_type is None):
            if(level is not None):
                max_question_level = max(
                    list(default_level_to_question_types.keys()))
                if level > max_question_level:
                    level = max_question_level
                question_type = default_level_to_question_types[level][0]
            else:
                question_type = random.choice(default_question_types)
        return question_type

    def _get_question(self, question_creator_node, data_question,
                      content_repository, user_id):
        """
        Go down the responsibility chain until we find a question that goes
        along with the data_question
        """
        while(question_creator_node):
            try:
                question_creator_class = question_creator_node.question_creator
                question_creator = question_creator_class(content_repository)
                question = question_creator.create(data_question, user_id)
                return question
            except QuestionCreatorException as ex:
                question_creator_node = question_creator_node.next

    def register_question_pack(self, code, question_pack):
        """
        Registers question_pack
        """
        self.question_pack_registry[code] = question_pack
