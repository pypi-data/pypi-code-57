import copy
import json
from typing import Dict

from pyllk.grammar import Grammar
from pyllk.production_rule import ExecutionContext, ProductionRule
from pyllk.token import NonTerminalToken, TerminalToken
from pyllk.token_stream import TokenStream


class Parser:
    grammar: Grammar
    debug = False

    def __init__(self, grammar: Grammar, debug=False):
        self.grammar = grammar
        self.debug = debug

    def parse(self, token_stream: TokenStream, context: Dict = {}):
        matched = self.consume_next_sub_rule(NonTerminalToken("INIT"), token_stream, context)
        return False if matched is None else True

    def parse_string(self, input: str, context: Dict = {}):
        '''Convenience method for parsing strings'''
        self.log(input)
        return self.parse(TokenStream([TerminalToken(c) for c in input]), context)

    def log(self, message: str):
        if self.debug:
            print(message)

    def consume_next_sub_rule(self, from_state: NonTerminalToken, token_stream: TokenStream, context: Dict = {}):
        if from_state.name not in self.grammar.lookup_table:
            raise Exception('UNKNOWN_STATE', 'The given state name {} is invalid'.format(from_state.name))

        rules = self.grammar.lookup_table[from_state.name]

        for rule in rules:
            self.log("Check rule({}) {}".format(token_stream.head, rule))
            consumed_tokens = self.consume(rule, token_stream, context)
            if consumed_tokens is not None:
                self.log("Consumed rule({}) {}".format(token_stream.head, rule))
                return consumed_tokens

    def consume(self, rule: ProductionRule, token_stream: TokenStream, context: Dict = {}):
        '''Tries to recursively consume a production rule. Returns False
        if it cannot do it and leaves the token stream at the position it
        initally found it by back-tracking.
        '''

        reset_head = token_stream.head
        reset_context = copy.deepcopy(context)
        self.log(json.dumps(reset_context))

        consumed_tokens = []

        for token in rule.produced:
            if isinstance(token, TerminalToken):
                if token.is_empty():
                    pass  # Empty matches every token
                elif (not token_stream.is_drained()) and (token.matches(token_stream.peek())):
                    tk = token_stream.consume()
                    consumed_tokens.append(tk)
                    self.log("Consumed token({}): {}".format(token_stream.head - 1, tk))
                else:
                    if self.debug:
                        if token_stream.is_drained():
                            self.log("Reset token stream to {} because drained stream".format(reset_head))
                        else:
                            self.log("Reset token stream to {} because of unmatched token: '{}'. Expected '{}'".format(reset_head, token_stream.peek(), token))

                    token_stream.set_to(reset_head)
                    context.clear()
                    for key in reset_context:
                        context[key] = reset_context[key]

                    return None
            else:
                sub_consumed_tokens = self.consume_next_sub_rule(token, token_stream, context)
                if sub_consumed_tokens is None:
                    self.log("Reset token stream to {}".format(reset_head))
                    token_stream.set_to(reset_head)
                    context.clear()
                    for key in reset_context:
                        context[key] = reset_context[key]

                    return None

                consumed_tokens.append(sub_consumed_tokens)

        if rule.action:
            # Rule is about to be accepted, execute the action if any.
            # Give the action the list of tokens it consumed
            self.log("EXECUTE({}) for {}".format(token_stream.head, rule))
            rule.action(ExecutionContext(self, rule, token_stream.tokens[reset_head:token_stream.head], context, consumed_tokens))

        return consumed_tokens


class Context(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
