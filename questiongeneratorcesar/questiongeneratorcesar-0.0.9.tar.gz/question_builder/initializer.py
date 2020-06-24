from question_builder.bp.question_builder import QuestionBuilder
from question_builder.data import DataQuestion, GetyarnContent, TwitterContent, QuestionPackRepository, ContentRepository
from question_builder.bp.question_pack import QuestionPack
from neo4j import GraphDatabase

def initialize_question_builder(config):
    content_driver = GraphDatabase.driver(config.uri_db, auth=(config.user_db, config.password_db))
    pack_driver = GraphDatabase.driver(config.uri_db, auth=(config.user_db, config.password_db))
    content_repository = ContentRepository(content_driver)
    question_builder = QuestionBuilder(content_repository)
    question_pack_repository = QuestionPackRepository(pack_driver)
    question_packs = question_pack_repository.get_question_packs()
    for qp_code, qp_config in question_packs.items(): 
        question_pack = QuestionPack(qp_code, qp_config)
        question_builder.register_question_pack(question_pack.code, question_pack)
    return question_builder