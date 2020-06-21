from rhme.hme_parser.grammar import yacc as yacc
from rhme.hme_parser.grammar import lex as lex
from rhme.hme_parser import base_grammar as base_grammar
from rhme import helpers
from rhme.helpers.exceptions import GrammarError, LexicalError, SintaticError
import numpy as np

class CheckLex():
    def __init__(self):
        self.__first_error = True
        self.latex_string=""
        self.latex=""
        self.latex_list=""
        self.attempts=0
        self.lex_error_list=None
        self.index=0
        self.token_errors_history=[]
        self.pure_lex_errors=[]

    def __locate_lex_error(self):
        helpers.debug("[check_grammar_lex.py] __locate_lex_error() | Locating all errors and creating a data structure.")

        error_list = self.lex_error_list.copy()
        latex = self.latex.copy()
        token_errors = []

        helpers.debug("[check_grammar_lex.py] __locate_lex_error() | List of lex errors:")
        helpers.debug(error_list)

        for error in error_list:

            if isinstance(error, dict):
                error = (error['label'], error['pos'])

            if error[1] != -1:
                helpers.debug("[check_grammar_lex.py] __locate_lex_error() | Locating error in latex_string.")
                latex_error_pos = error[1]
                latex_error = self.latex_string[latex_error_pos::]
                latex_error_token = error[0]

                count = 0
                count_list = 0

                helpers.debug("[check_grammar_lex.py] __locate_lex_error() | Searching token (in latex) with position returned in error.")
                for symbol in latex:

                    if symbol['label'] != latex_error_token:
                        # Increment counter if current position is the position containing the error
                        count += len(symbol['label'])
                        count_list += 1
                    elif count == latex_error_pos:
                        token_errors.append({
                            'pos': latex_error_pos,
                            'pos_list': count_list,
                            'label': symbol['label'],
                            'prediction': symbol['prediction'],
                            'attempts': [latex_error_pos] # Stores the symbol attempts to restore the grammar
                        })
                        self.token_errors_history.extend(token_errors)
                        break
            else:
                helpers.debug("[check_grammar_lex.py] __locate_lex_error() | Cannot fix the error. Use an automata do fix it. Logging the error:")
                helpers.debug(error)
                continue

        return token_errors, self.token_errors_history

    def check_correct_lex(self):
        """Check and correct lex errors

        Args:
            latex_string (str): Latex string.
            latex (list): First latex structure.
            latex_list (list): [description]

        Returns:
            latex_string (str):
            token_errors (list): 
            token_errors_history (list):
            latex (list):
            latex_list (list):
        """

        helpers.debug("[check_grammar_lex.py] check_correct_lex()")
        helpers.debug("[check_grammar_lex.py] check_correct_lex() | attempts: %s" % self.attempts)
        helpers.debug("[check_grammar_lex.py] check_correct_lex() | error list:")
        helpers.debug(self.lex_error_list)
        helpers.debug(self.__first_error)

        second_lex_error_list = None
        token_errors = []

        if not self.lex_error_list and self.__first_error and self.attempts < 3:

            helpers.debug("[check_grammar_lex.py] check_correct_lex() | There's no previous error. Searching the first one.")

            lex_error_list = lex.LatexLexer(self.latex_string)
            helpers.debug("[check_grammar_lex.py] check_correct_lex() | error:")
            helpers.debug(lex_error_list)

            self.pure_lex_errors.append(lex_error_list)
            self.lex_error_list = lex_error_list

            if self.lex_error_list:
                helpers.debug("[check_grammar_lex.py] check_correct_lex() | First error found in lex.")
                token_errors, self.token_errors_history = self.__locate_lex_error()

                self.__first_error = False
                self.__attempt_to_fix_error(token_errors)

                if token_errors:
                    raise LexicalError({
                        'error': token_errors,
                        'latex': self.latex,
                        'latex_list': self.latex_list,
                        'token_errors_history': self.token_errors_history,
                        'latex_string': self.latex_string,
                        'pure_lex_errors_list': self.pure_lex_errors
                    })

        elif self.lex_error_list and not self.__first_error and self.attempts < 3:
            helpers.debug("[check_grammar_lex.py] check_correct_lex() | There's previous error. Searching for new errors.")

            second_lex_error_list = lex.LatexLexer(self.latex_string)
            self.pure_lex_errors.append(second_lex_error_list)

            if second_lex_error_list:
                helpers.debug("[check_grammar_lex.py] check_correct_lex() | New errors found.")

                ''' 
                    If new error is EOF error
                    Remove the error from the list. Takes the next one.
                '''
                if second_lex_error_list[0][1] == -1:
                    second_lex_error_list.reverse()
                    second_lex_error_list.pop()
                    second_lex_error_list.reverse()

                self.lex_error_list = second_lex_error_list

                token_errors, self.token_errors_history = self.__locate_lex_error()

                self.__attempt_to_fix_error(token_errors)

                raise LexicalError({
                    'error': token_errors,
                    'latex': self.latex,
                    'latex_list': self.latex_list,
                    'token_errors_history': self.token_errors_history,
                    'latex_string': self.latex_string,
                    'pure_lex_errors_list': self.pure_lex_errors
                })

        elif self.lex_error_list and self.attempts >= 3:
            raise LexicalError({
                'error': token_errors, # ?
                'latex': self.latex,
                'latex_list': self.latex_list,
                'token_errors_history': self.token_errors_history,
                'latex_string': self.latex_string,
                'pure_lex_errors_list': self.pure_lex_errors
            })

        return self.latex_string, token_errors, self.token_errors_history, self.latex, self.latex_list

    def __attempt_to_fix_error(self, token_errors):
        helpers.debug("[check_grammar_lex.py] self.__attempt_to_fix_error() | Tries to fix the error.")

        # Tenta resolver o primeiro erro e retorna a lista de erros atualizada
        bg = base_grammar.BaseGrammar()
        update_latex_string, updated_lex_error_list, self.index = bg.correct_grammar_lex(token_errors, self.latex, self.latex_list, 0)

        helpers.debug("[check_grammar_lex.py] self.__attempt_to_fix_error() | Save errors in history.")
        self.lex_error_list = updated_lex_error_list
        if updated_lex_error_list:
            self.token_errors_history = updated_lex_error_list

        if update_latex_string:
            self.latex_string = update_latex_string
            self.attempts += 1
            helpers.debug("[check_grammar_lex.py] self.__attempt_to_fix_error() | Recursion. Check tokens again.")
            return self.check_correct_lex()