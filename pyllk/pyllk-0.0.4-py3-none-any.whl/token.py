class Token:
    pass


class TerminalToken(Token):
    representation: object

    def __init__(self, representation: object):
        self.representation = representation

    def __eq__(self, obj):
        return self.representation == obj

    def __str__(self):
        return self.representation

    def matches(self, obj):
        return self == obj

    def is_empty(self):
        '''Override this method to provide a different implementation of empty
        '''
        return self == ''


class NonTerminalToken(Token):
    name: str

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "[{}]".format(self.name)
