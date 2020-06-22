import re
from enum import Enum, auto


class LexError(Exception):
    pass


class Token(Enum):
    TTYPE = auto()
    TENUM = auto()
    TNAME = auto()
    TINTEGER = auto()
    TU8 = auto()
    TU16 = auto()
    TU32 = auto()
    TU64 = auto()
    TI8 = auto()
    TI16 = auto()
    TI32 = auto()
    TI64 = auto()
    TF32 = auto()
    TF64 = auto()
    TE8 = auto()
    TE16 = auto()
    TE32 = auto()
    TE64 = auto()
    TBOOL = auto()
    TSTRING = auto()
    TDATA = auto()
    TMAP = auto()
    TOPTIONAL = auto()
    TLANGLE = auto()
    TRANGLE = auto()
    TLBRACE = auto()
    TRBRACE = auto()
    TLBRACKET = auto()
    TRBRACKET = auto()
    TLPAREN = auto()
    TRPAREN = auto()
    TCOMMA = auto()
    TPIPE = auto()
    TEQUAL = auto()
    TCOLON = auto()


RE_TSTRING = re.compile('[a-zA-Z0-9_]+')
RE_TINTEGER = re.compile('[0-9]+')


class LexedToken:
    def __init__(self, token, value, line, column):
        self.token = token
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return '<LexedToken {} "{}" at {},{}>'.format(self.token, self.value, self.line, self.column)


def _lex_string(data, line, column):
    if data == 'type':
        return LexedToken(Token.TTYPE, "", line, column)
    elif data == 'enum':
        return LexedToken(Token.TENUM, "", line, column)
    elif data == 'u8':
        return LexedToken(Token.TU8, "", line, column)
    elif data == 'u16':
        return LexedToken(Token.TU16, "", line, column)
    elif data == 'u32':
        return LexedToken(Token.TU32, "", line, column)
    elif data == 'u64':
        return LexedToken(Token.TU64, "", line, column)
    elif data == 'i8':
        return LexedToken(Token.TI8, "", line, column)
    elif data == 'i16':
        return LexedToken(Token.TI16, "", line, column)
    elif data == 'i32':
        return LexedToken(Token.TI32, "", line, column)
    elif data == 'i64':
        return LexedToken(Token.TI64, "", line, column)
    elif data == 'f32':
        return LexedToken(Token.TF32, "", line, column)
    elif data == 'f64':
        return LexedToken(Token.TF64, "", line, column)
    elif data == 'e8':
        return LexedToken(Token.TE8, "", line, column)
    elif data == 'e16':
        return LexedToken(Token.TE16, "", line, column)
    elif data == 'e32':
        return LexedToken(Token.TE32, "", line, column)
    elif data == 'e64':
        return LexedToken(Token.TE64, "", line, column)
    elif data == 'bool':
        return LexedToken(Token.TBOOL, "", line, column)
    elif data == 'string':
        return LexedToken(Token.TSTRING, "", line, column)
    elif data == 'data':
        return LexedToken(Token.TDATA, "", line, column)
    elif data == 'optional':
        return LexedToken(Token.TOPTIONAL, "", line, column)
    elif data == 'map':
        return LexedToken(Token.TMAP, "", line, column)
    else:
        return LexedToken(Token.TNAME, data, line, column)


def lex_schema(data):
    pointer = 0
    line = 1
    column = 0
    while True:
        if pointer == len(data):
            return
        if data[pointer] == ' ' or data[pointer] == '\t':
            pass
        elif data[pointer] == '\n':
            column = 0
            line += 1
            pointer += 1
            continue
        elif data[pointer].isalpha():
            part = RE_TSTRING.search(data[pointer:])[0]
            yield _lex_string(part, line, column)
            column += len(part) - 1
            pointer += len(part) - 1
        elif data[pointer].isdigit():
            part = RE_TINTEGER.search(data[pointer:])[0]
            yield LexedToken(Token.TINTEGER, part, line, column)
            column += len(part) - 1
            pointer += len(part) - 1
        elif data[pointer] == '#':
            while data[pointer] != '\n':
                pointer += 1
            line += 1
            pointer += 1
            column = 0
            continue
        elif data[pointer] == '<':
            yield LexedToken(Token.TLANGLE, "", line, column)
        elif data[pointer] == '>':
            yield LexedToken(Token.TRANGLE, "", line, column)
        elif data[pointer] == '{':
            yield LexedToken(Token.TLBRACE, "", line, column)
        elif data[pointer] == '}':
            yield LexedToken(Token.TRBRACE, "", line, column)
        elif data[pointer] == '[':
            yield LexedToken(Token.TLBRACKET, "", line, column)
        elif data[pointer] == ']':
            yield LexedToken(Token.TRBRACKET, "", line, column)
        elif data[pointer] == '(':
            yield LexedToken(Token.TLPAREN, "", line, column)
        elif data[pointer] == ')':
            yield LexedToken(Token.TRPAREN, "", line, column)
        elif data[pointer] == ',':
            yield LexedToken(Token.TCOMMA, "", line, column)
        elif data[pointer] == '|':
            yield LexedToken(Token.TPIPE, "", line, column)
        elif data[pointer] == '=':
            yield LexedToken(Token.TEQUAL, "", line, column)
        elif data[pointer] == ':':
            yield LexedToken(Token.TCOLON, "", line, column)
        else:
            raise LexError("Parse error at {},{}".format(line, column))

        pointer += 1
        column += 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('schema', help='Schema file to lex')
    args = parser.parse_args()
    with open(args.schema) as handle:
        raw = handle.read()

    for token in lex_schema(raw):
        print(token)
