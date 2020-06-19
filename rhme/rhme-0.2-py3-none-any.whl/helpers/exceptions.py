import json

class GrammarError(Exception):
    def __init__(self, valor="Could not solve the grammar error", data=None):
        self.valor = valor
        self.data = data
    def __repr__(self):
        return {
            'message': self.valor,
            'data': self.data
        }
    def __str__(self):
        return self.__repr__()

class SintaticError(Exception):
    def __init__(self, valor="Could not solve the sintatic error", data=None):
        self.valor = valor
        self.data = data
    def __repr__(self):
        return {
            'message': self.valor,
            'data': self.data
        }
    def __str__(self):
        return self.__repr__()

class LexicalError(Exception):
    def __init__(self, valor="Could not solve the lexical error", data=None):
        self.valor = valor
        self.data = data
    def __repr__(self):
        return {
            'message': self.valor,
            'data': self.data
        }
    def __str__(self):
        return self.__repr__()
