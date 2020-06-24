from rhme import helpers
from rhme.hme_parser import check_grammar_lex as check_grammar_lex
from rhme.hme_parser import check_grammar_sintax as check_grammar_sintax
from rhme.helpers.exceptions import GrammarError, LexicalError, SintaticError

class CheckGrammar():

    def __init__(self):
        self.__attempts_lex = 0
        self.__attempts_grammar = 0
        self.lex_errors=None
        self.pure_lex_errors=None
        self.yacc_errors=None
        self.pure_yacc_errors=None

    def __remove_contains(self, tstring):
        if isinstance(tstring, str):
            tstring = tstring.replace('contains', '')
        elif isinstance(tstring, list) and "contains" in tstring:
            tstring = tstring.remove('contains')
        return tstring

    def check(self, tstring):
        helpers.debug("[check_grammar.py] check()")

        latex = []
        latex_list = []

        for symbol in tstring:
            if symbol['label'] != '' and symbol['label'] != 'contains':
                latex.append(symbol)
                latex_list.append(symbol['label'])


        latex_string = "".join(latex_list)
        latex_string = self.__remove_contains(latex_string)
        lstring = latex_string

        helpers.debug("[check_grammar.py] check() | Latex List:")
        helpers.debug(latex_list)
        helpers.debug("[check_grammar.py] check() | Latex String: %s " % latex_string)

        '''
        Latex: {'label': symbol, 'prediction': [], 'type': 'context'}
        Latex List: ['\sqrt','{','9','}']
        Latex String: '\sqrt{9}'
        '''

        try:
            new_latex_string, token_errors, token_errors_history, latex, latex_list = self.__check_lex(latex_string, latex, latex_list)
            helpers.debug('[check_grammar.py] check() | after check lex')
            self.lex_errors = token_errors_history

            helpers.debug("[check_grammar.py] check() | ...........")

            if not token_errors:
                new_latex_string, grammar_errors, grammar_errors_history, latex, latex_list = self.__check_yacc(token_errors_history, new_latex_string, latex, latex_list)
                self.yacc_errors = grammar_errors_history

            else:
                raise LexicalError(data={
                    'error': token_errors,
                    'latex': latex,
                    'latex_list': latex_list,
                    'token_errors_history': token_errors_history,
                    'latex_string': latex_string,
                    'new_latex_string': new_latex_string
                })

            if new_latex_string != -1 and new_latex_string != None:
                lstring = new_latex_string

            return lstring
        except Exception as e:
            e.data.update({'latex_string_original': latex_string})
            helpers.debug('[check_grammar.py] check() | Exception:')
            helpers.debug(e)
            raise e

    def __check_lex(self, latex_string, latex, latex_list):
        cgl = check_grammar_lex.CheckLex()
        cgl.latex_string = latex_string
        cgl.latex = latex
        cgl.latex_list = latex_list
        cgl.attempts = self.__attempts_lex
        new_latex_string, token_errors, token_errors_history, latex, latex_list = cgl.check_correct_lex()
        self.pure_lex_errors = cgl.pure_lex_errors
        return new_latex_string, token_errors, token_errors_history, latex, latex_list

    def __check_yacc(self, token_errors_history, new_latex_string, latex, latex_list):
        symbols_attempts_in_lex = []
        for token in token_errors_history:
            symbols_attempts_in_lex.extend(token['attempts'])

        cgs = check_grammar_sintax.CheckSintax()
        cgs.latex_string = new_latex_string
        cgs.latex = latex
        cgs.latex_list = latex_list
        cgs.attempts = self.__attempts_grammar
        cgs.symbols_attempts_in_lex = symbols_attempts_in_lex                
        result = cgs.check_correct_grammar()
        self.pure_yacc_errors = cgs.pure_yacc_errors
        return result