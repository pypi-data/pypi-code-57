from collections import namedtuple, defaultdict
import logging
from .data_question import DataQuestion
from . import queries
from .content import TwitterContent, GetyarnContent
import time

CONTENT_LIST_KEY = "content_list"
CONTENT_KEY = "content"
INTEREST_KEY = "interest"
WORD_KEY = "word"
LEMMA_KEY = "lemma"
SOURCE_KEY = "source"
GETYARN_KEY = "getyarn"
TWITTER_KEY = "twitter"
ID_KEY = "id"
POS_KEY = "pos"
PHRASE_KEY = "phrase"
TRANSLATION_KEY = "translation"
IMAGE_LINK_KEY = "image_link"
MEDIA_TYPE_KEY = "media_type"
TWEET_URL_KEY = "tweet_url"
MASTERED_KEY = "mastered"
LEVEL_KEY = "level"
TEXT = "text"

Q_VARIABLE_KEY = "qu"

N_INTEREST_TYPES = 3

LemmaData = namedtuple("LemmaData", ["data_question", "level", "mastered"])


class ContentRepository():
    """
    Handles all the db operations related to user content management
    """
    def __init__(self, driver):
        """
        Initializes the neo4j db
        """
        self._driver = driver

    def get_lexemas_from_lemma(self, lemma):
        lexemas = []
        with self._driver.session() as session:
            for res in session.read_transaction(self._get_lexemas_from_lemma,
                                                lemma):
                lexemas.append(res)
        return lexemas

    @staticmethod
    def _get_lexemas_from_lemma(tx, lemma):
        query = queries.GET_LEXEMAS_FROM_LEMMA.format(lemma)
        return tx.run(query)

    def get_random_questions_by_pos_without_lexemas(self, word_set, user_id,
                                                    n_questions):
        lemma_to_question = defaultdict()
        with self._driver.session() as session:
            for res in session.read_transaction(
                    self._get_random_questions_by_pos_without_lexemas,
                    word_set, user_id, n_questions):
                target_lemma = res[WORD_KEY][TEXT]
                content_rel_json = res[CONTENT_KEY]
                content_rel_json[LEMMA_KEY] = target_lemma
                lemma_to_question[target_lemma] = self._to_question(
                    content_rel_json)
        return lemma_to_question

    @staticmethod
    def _get_random_questions_by_pos_without_lexemas(tx, word_set, user_id,
                                                     n_questions):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS_WITHOUT_LEXEMAS.format(   # noqa: E501
            word_set, user_id, int(n_questions/N_INTEREST_TYPES))
        return tx.run(query)

    def get_random_questions_by_pos(self, word_set, user_id, n_questions):
        lemma_to_question = defaultdict()
        with self._driver.session() as session:
            for res in session.read_transaction(
                    self._get_random_questions_by_pos, word_set, user_id,
                    n_questions):
                target_lemma = res[WORD_KEY][TEXT]
                content_rel_json = res[CONTENT_KEY]
                content_rel_json[LEMMA_KEY] = target_lemma
                lemma_to_question[target_lemma] = self._to_question(
                    content_rel_json)
        return lemma_to_question

    @staticmethod
    def _get_random_questions_by_pos(tx, word_set, user_id, n_questions):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS.format(
            word_set, user_id, int(n_questions/N_INTEREST_TYPES))
        return tx.run(query)

    def get_random_questions(self, lemma_list, user_id, n_questions):
        lemma_to_question = defaultdict()
        s1 = time.perf_counter()
        with self._driver.session() as session:
            for res in session.read_transaction(
                    self._get_random_questions, user_id, lemma_list,
                    n_questions):
                target_lemma = res[LEMMA_KEY]
                target_word = res[WORD_KEY]
                content_rel_json = res[CONTENT_KEY]
                content_rel_json[LEMMA_KEY] = target_lemma
                mastered = res[MASTERED_KEY]
                level = res[LEVEL_KEY]
                mastered = mastered if mastered else False
                level = level if level else 1
                lemma_to_question[target_lemma] = LemmaData(
                    self._to_question(content_rel_json), level, mastered)
        return lemma_to_question

    @staticmethod
    def _get_random_questions(tx, word_list, user_id, n_questions):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT.format(
            word_list, user_id, int(n_questions/N_INTEREST_TYPES))
        return tx.run(query)

    def get_random_questions_paginated(self, word_list, user_id, page,
                                       max_items_per_page):
        question_list = []
        with self._driver.session() as session:
            for res in session.read_transaction(
                    self._get_random_questions_paginated, word_list, user_id,
                    page, max_items_per_page):
                for content_rel_json in res[CONTENT_LIST_KEY]:
                    question_list.append(self._to_question(content_rel_json))
        return page, question_list

    @staticmethod
    def _get_random_questions_paginated(tx, word_list, user_id, page,
                                        max_items_per_page):
        n_questions = int(max_items_per_page/len(word_list))
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_PAGINATED.\
            format(word_list, user_id, page*n_questions, n_questions)
        return tx.run(query)

    def get_question(self, uid, word):
        with self._driver.session() as session:
            for res in session.read_transaction(self._get_random_question, uid,
                                                word):
                content_rel_json = res[Q_VARIABLE_KEY]
                question = self._to_question(content_rel_json)
                return question

    @staticmethod
    def _get_random_question(tx, uid, word):
        query = queries.GET_QUESTION_FROM_USER.format(uid, word)
        results = tx.run(query)
        return results

    def words_have_content(self, user_id, words):
        with self._driver.session() as session:
            content = session.read_transaction(self._words_have_content,
                                               user_id, words)
            words_with_content = [word[0] for word in content.values()]
            return words_with_content

    @staticmethod
    def _words_have_content(tx, user_id, words):
        query = queries.CHECK_WORDS_CONTENT.format(user_id, words)
        return tx.run(query)

    @staticmethod
    def _to_content(content_rel_json):
        content_json = content_rel_json[CONTENT_KEY]
        source = content_json[SOURCE_KEY]
        if(source == GETYARN_KEY):
            content = GetyarnContent(content_json[ID_KEY],
                                     content_json[PHRASE_KEY],
                                     content_json[TRANSLATION_KEY],
                                     content_json[MEDIA_TYPE_KEY],
                                     content_json[SOURCE_KEY])
        elif(source == TWITTER_KEY):
            content = TwitterContent(content_json[ID_KEY],
                                     content_json[IMAGE_LINK_KEY],
                                     content_json[PHRASE_KEY],
                                     content_json[MEDIA_TYPE_KEY],
                                     content_json[TWEET_URL_KEY],
                                     content_json[SOURCE_KEY])
        return content

    @staticmethod
    def _to_question(content_rel_json):
        content = ContentRepository._to_content(content_rel_json)
        interest = content_rel_json[INTEREST_KEY]
        target_lemma = content_rel_json[LEMMA_KEY]
        target_word = content_rel_json[WORD_KEY]
        pos = content_rel_json[POS_KEY]
        return DataQuestion(content, interest, target_lemma, target_word, pos)

    def get_question_packs(self):
        question_packs = {}
        with self._driver.session() as session:
            for res in session.read_transaction(self._get_question_packs):
                question_pack_code = res["question_pack"]["code"]
                level = res["level"]
                for question_type in res["question_types"]:
                    if question_pack_code not in question_packs:
                        question_packs[question_pack_code] = defaultdict(list)
                    if question_type["enabled"]:
                        question_packs[question_pack_code][level].append(
                            question_type["code"])
        return question_packs

    @staticmethod
    def _get_question_packs(tx):
        query = queries.GET_QUESTION_PACKS
        results = tx.run(query)
        return results
