from bare.lex import lex_schema, Token
from bare.ast import BareType, BareEnum, BarePrimitive, TypeKind, OptionalType, StructType, NamedType, ArrayType, \
    MapType, EnumValue, UnionType


class UnexpectedTokenError(Exception):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected
        msg = 'Unexpected token {}, expected {} (at {}, {})'.format(token.token, expected, token.line, token.column)
        super().__init__(msg)


class PeekableGenerator(object):

    def __init__(self, generator):
        self.empty = False
        self.peek = None
        self.generator = generator
        try:
            self.peek = self.generator.__next__()
        except StopIteration:
            self.empty = True

    def __iter__(self):
        return self

    def __next__(self):
        """
        Return the self.peek element, or raise StopIteration
        if empty
        """
        if self.empty:
            raise StopIteration()
        to_return = self.peek
        try:
            self.peek = self.generator.__next__()
        except StopIteration:
            self.peek = None
            self.empty = True
        return to_return


def parse(schema):
    tokens = PeekableGenerator(lex_schema(schema))
    types = []
    while True:
        try:
            st = _parse_schema_type(tokens)
        except StopIteration:
            break
        types.append(st)
    return types


def _parse_schema_type(tokens):
    token = tokens.__next__()

    if token.token == Token.TTYPE:
        return _parse_schema_user_type(tokens)
    elif token.token == Token.TENUM:
        return _parse_schema_user_enum(tokens)
    else:
        raise UnexpectedTokenError(token, "'type' or 'enum'")


def _parse_schema_user_type(tokens):
    token = tokens.__next__()
    if token.token != Token.TNAME:
        raise UnexpectedTokenError(token, 'type name')

    new_type = BareType()
    new_type.name = token.value
    new_type.type = _parse_type(tokens)
    return new_type


def _parse_schema_user_enum(tokens):
    token = tokens.__next__()
    if token.token != Token.TNAME:
        raise UnexpectedTokenError(token, 'enum name')

    new_enum = BareEnum()
    new_enum.name = token.value

    token = tokens.__next__()
    if token.token == Token.TE8:
        new_enum.type = TypeKind.E8
    elif token.token == Token.TE16:
        new_enum.type = TypeKind.E16
    elif token.token == Token.TE32:
        new_enum.type = TypeKind.E32
    elif token.token == Token.TE64:
        new_enum.type = TypeKind.E64
    else:
        raise UnexpectedTokenError(token, 'enum type')

    token = tokens.__next__()
    if token.token != Token.TLBRACE:
        raise UnexpectedTokenError(token, '{')

    value = 0
    while True:
        token = tokens.__next__()
        if token.token == Token.TRBRACE:
            break
        if token.token != Token.TNAME:
            raise UnexpectedTokenError(token, 'value name')

        value_name = token.value

        if tokens.peek.token == Token.TEQUAL:
            tokens.__next__()
            token = tokens.__next__()
            if token.token != Token.TINTEGER:
                raise UnexpectedTokenError(token, 'integer')
            new_enum.values.append(EnumValue(value_name, int(token.value)))
        else:
            new_enum.values.append(EnumValue(value_name, value))
            value += 1
    return new_enum


def _parse_type(tokens, allow_tname=False):
    token = tokens.__next__()
    if token.token == Token.TU8:
        return BarePrimitive(TypeKind.U8)
    elif token.token == Token.TU16:
        return BarePrimitive(TypeKind.U16)
    elif token.token == Token.TU32:
        return BarePrimitive(TypeKind.U32)
    elif token.token == Token.TU64:
        return BarePrimitive(TypeKind.U64)
    elif token.token == Token.TI8:
        return BarePrimitive(TypeKind.I8)
    elif token.token == Token.TI16:
        return BarePrimitive(TypeKind.I16)
    elif token.token == Token.TI32:
        return BarePrimitive(TypeKind.I32)
    elif token.token == Token.TI64:
        return BarePrimitive(TypeKind.I64)
    elif token.token == Token.TF32:
        return BarePrimitive(TypeKind.F32)
    elif token.token == Token.TF64:
        return BarePrimitive(TypeKind.F64)
    elif token.token == Token.TE8:
        return BarePrimitive(TypeKind.E8)
    elif token.token == Token.TE16:
        return BarePrimitive(TypeKind.E16)
    elif token.token == Token.TE32:
        return BarePrimitive(TypeKind.E32)
    elif token.token == Token.TE64:
        return BarePrimitive(TypeKind.E64)
    elif token.token == Token.TBOOL:
        return BarePrimitive(TypeKind.Bool)
    elif token.token == Token.TSTRING:
        return BarePrimitive(TypeKind.String)
    elif token.token == Token.TOPTIONAL:
        token = tokens.__next__()
        if token.token != Token.TLANGLE:
            raise UnexpectedTokenError(token, "<")
        subtype = _parse_type(tokens)
        token = tokens.__next__()
        if token.token != Token.TRANGLE:
            raise UnexpectedTokenError(Token, ">")
        return OptionalType(subtype)
    elif token.token == Token.TDATA:
        if tokens.peek.token == Token.TLANGLE:
            tokens.__next__()
            token = tokens.__next__()
            if token.token != Token.TINTEGER:
                raise UnexpectedTokenError(token, 'length')
            length = int(token.value)
            token = tokens.__next__()
            if token.token != Token.TRANGLE:
                raise UnexpectedTokenError(token, '>')
            return BarePrimitive(TypeKind.DataFixed, length=length)
        else:
            return BarePrimitive(TypeKind.Data)
    elif token.token == Token.TLBRACE:
        return _parse_struct(tokens)
    elif token.token == Token.TLBRACKET:
        token = tokens.__next__()
        if token.token == Token.TRBRACKET:
            subtype = _parse_type(tokens)
            return ArrayType(subtype)
        elif token.token == Token.TINTEGER:
            token = tokens.__next__()
            length = int(token.value)
            token = tokens.__next__()
            if token.token != Token.TRBRACKET:
                raise UnexpectedTokenError(token, ']')
            subtype = _parse_type(tokens)
            return ArrayType(subtype, length)
        else:
            raise UnexpectedTokenError(token, "']' or array length")
    elif token.token == Token.TMAP:
        token = tokens.__next__()
        if token.token != Token.TLBRACKET:
            raise UnexpectedTokenError(token, '[')
        keytype = _parse_type(tokens)
        token = tokens.__next__()
        if token.token != Token.TRBRACKET:
            raise UnexpectedTokenError(token, ']')
        valuetype = _parse_type(tokens)
        return MapType(keytype, valuetype)
    elif token.token == Token.TLPAREN:
        types = []
        while True:
            types.append(_parse_type(tokens, allow_tname=True))
            token = tokens.__next__()
            if token.token == Token.TPIPE:
                continue
            elif token.token == Token.TRPAREN:
                break
            else:
                raise UnexpectedTokenError(token, "'|' or ')'")
        return UnionType(types)
    elif token.token == Token.TNAME and allow_tname:
        return NamedType(token.value)
    else:
        raise UnexpectedTokenError(token, 'a type')


def _parse_struct(tokens):
    result = StructType()
    while True:
        token = tokens.__next__()
        if token.token == Token.TRBRACE:
            return result
        if token.token != Token.TNAME:
            raise UnexpectedTokenError(token, 'field name')
        name = token.value

        token = tokens.__next__()
        if token.token != Token.TCOLON:
            raise UnexpectedTokenError(token, ':')

        if tokens.peek.token == Token.TNAME:
            token = tokens.__next__()
            result.fields[name] = NamedType(token.value)
        else:
            result.fields[name] = _parse_type(tokens)

        if tokens.peek.token == Token.TCOMMA:
            tokens.__next__()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('schema', help='Schema file to parse')
    args = parser.parse_args()
    with open(args.schema) as handle:
        raw = handle.read()

    for defined_type in parse(raw):
        print(defined_type)
