import cv2 as cv
from rhme import helpers
from rhme.hme_parser import parser as parser
from rhme.recognize import *
from rhme.config import Configuration as config

class HME_Recognizer:

    def __init__(self):
        self.reset()

    def __to_parse(self, expression):
        try:
            parse = parser.Parser(expression)
            to_parse = parse.to_parse()

            parsed_expression = to_parse['latex']

            self.expression_after_parser = to_parse['latex_before_cg']
            self.expression_after_grammar = parsed_expression
            self.parser_tree = parse.tree
            self.parser_list = parse.tlist
            self.lex_errors = to_parse['lex_errors']
            self.pure_lex_errors = to_parse['pure_lex_errors']
            self.yacc_errors = to_parse['yacc_errors']
            self.pure_yacc_errors = to_parse['pure_yacc_errors']

            return parsed_expression

        except Exception as e:
            print("[api.py] __to_parse | Exception:")
            raise e

    def recognize(self, image):
        try:
            if isinstance(image, str):
                image = cv.imread(image, 0)
            else:
                image = image.copy()

            self.image = image

            if self.image is not None:
                hme = Recognize(image)

                expression, image = hme.to_recognize()

                self.expression_after_recognition = expression.copy()
                self.predictions = hme.prediction

                parsed_expression = self.__to_parse(expression)

                self.parsed_expression = parsed_expression
                self.processed_image = image

                return parsed_expression, image
            else:
                print("[api.py] recognize | Exception:")
                raise Exception("You must enter an image.")
        except Exception as e:
            print("[api.py] recognize | Exception:")
            raise e

    def reset(self):
        self.image=None
        self.parsed_expression=""
        self.processed_image=None
        self.predictions=None
        self.configurations=None
        self.expression_after_recognition={} 
        self.expression_after_parser=[]
        self.expression_after_grammar=""
        self.parser_tree=None
        self.parser_list=None
        self.lex_errors=None
        self.yacc_errors=None
        self.pure_lex_errors=None
        self.pure_yacc_errors=None

    def get_predictions(self):
        return self.predictions

    def get_labels(self):
        labels = helpers.get_labels()
        return labels

    def get_expression_before_parser(self):
        return self.expression_before_parser

    def get_expression_after_parser(self):
        return self.expression_after_parser

    def get_expression_before_grammar(self):
        return self.expression_before_grammar

    def get_expression_after_grammar(self):
        return self.expression_after_grammar

    def get_lex_errors(self):
        return self.lex_errors

    def get_yacc_errors(self):
        return self.yacc_errors

    def get_pure_lex_errors(self):
        return self.pure_lex_errors

    def get_pure_yacc_errors(self):
        return self.pure_yacc_errors

    def configuration(self):
        return config
