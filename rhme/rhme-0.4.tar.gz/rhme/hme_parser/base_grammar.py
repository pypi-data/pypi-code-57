import numpy as np
from rhme import helpers
from rhme.hme_parser.grammar import lex as lex
from rhme.hme_parser.grammar import yacc as yacc

helpers_labels = helpers.get_labels()
labels = helpers_labels['labels_parser']

class BaseGrammar():

    def __init__(self):
        pass

    def correct_grammar_lex(self, token_errors, latex, latex_list, index=0, previous_attemptions=[]):
        """Fix grammar and lex errors.
        It tries to fix one error at the time. 
        The error index is passed as parameter, otherwise, the first error (index=0) will be used.

        Args:
            token_errors (list): Errors found in previous step: either check_grammar_lex.py or check_grammar_sintax.py
            latex (list): First latex structure.
            latex_list (list): [description]
            index (int, optional): Index of error. Default to 0.
            previous_attemptions (list, optional): This list stores all previous symbol (index) attemptions to fix the error. Defaults to [].

        Returns:
            latex_string, token_errors, index: Updated data.
        """
        latex_string = ""

        helpers.debug("[base_grammar.py] correct_grammar_lex()")
        helpers.debug("[base_grammar.py] correct_grammar_lex() | List of errors:")
        helpers.debug(token_errors)

        if len(token_errors) > 0:

            pos = token_errors[index]['pos']
            pos_list = token_errors[index]['pos_list']
            pred = token_errors[index]['prediction'].copy()

            helpers.debug("[base_grammar.py] correct_grammar_lex() | Error position")

            # colocar em um helpers
            subst = helpers.subst

            if not isinstance(pred, list): # When there's predictions it is a numpy array, not a list.

                json_label = 'labels_parser'

                def get_new_index(pred):
                    helpers.debug("[base_grammar.py] correct_grammar_lex() | Reset prediction of current symbol")
                    new_pred = pred.copy()
                    new_pred[0][np.argmax(pred)] = 0
                    helpers.debug("[base_grammar.py] correct_grammar_lex() | Gets new indx and prediction from next index with higher prediction")
                    new_index = np.argmax(new_pred)
                    return new_index, new_pred

                def recur_get_new_index(pred):
                    new_index, pred = get_new_index(pred)
                    if new_index in token_errors[index]['attempts'] or new_index in previous_attemptions:
                        helpers.debug("[base_grammar.py] correct_grammar_lex() | New index is in previous attempts. Getting next.")
                        return recur_get_new_index(pred)
                    else:
                        label_recog = helpers_labels[json_label][str(new_index)]
                        new_label = helpers_labels["labels_recognition"][label_recog]
                        new_identification = labels[new_label]
                        helpers.debug("[base_grammar.py] correct_grammar_lex() | New symbol identification: %s " % new_identification)
                        return new_index, pred, new_identification

                new_index, new_pred, new_identification = recur_get_new_index(pred)

                helpers.debug("[base_grammar.py] correct_grammar_lex() | Updated symbol prediction")
                token_errors[index]['prediction'] = new_pred

                helpers.debug("[base_grammar.py] correct_grammar_lex() | Store new index attempt")
                token_errors[index]['attempts'].append(new_index)

                helpers.debug("[base_grammar.py] correct_grammar_lex() | Updated 'latex' and 'latex_list'. It is NOT a copy so, it is already updated.")

                # Make ir more 'Pythonic' later
                if new_identification in subst:
                    substitution_list = subst[new_identification] # list of substitutions
                    for substitution_index in range(0, len(substitution_list)):
                        for substitution in substitution_list[substitution_index]:
                            if new_identification == substitution:
                                new_identification = substitution_list[substitution_index][substitution]

                latex_list[pos_list] = new_identification
                latex[pos_list]['label'] = new_identification
                latex[pos_list]['prediction'] = new_pred

                helpers.debug("[base_grammar.py] correct_grammar_lex() | Creating new 'latex_string' from 'latex_list'")
                latex_string = latex_string.join(latex_list)

        return latex_string, token_errors, index