import argparse
import bare.parser
from bare.ast import BareType, BarePrimitive, StructType, TypeKind


def _gen_format(typekind, length):
    if typekind == TypeKind.U8 or typekind == TypeKind.E8:
        return 'B'
    elif typekind == TypeKind.U16 or typekind == TypeKind.E16:
        return 'H'
    elif typekind == TypeKind.U32 or typekind == TypeKind.E32:
        return 'I'
    elif typekind == TypeKind.U64 or typekind == TypeKind.E64:
        return 'Q'
    elif typekind == TypeKind.I8:
        return 'b'
    elif typekind == TypeKind.I16:
        return 'h'
    elif typekind == TypeKind.I32:
        return 'i'
    elif typekind == TypeKind.I64:
        return 'q'
    elif typekind == TypeKind.F32:
        return 'f'
    elif typekind == TypeKind.F64:
        return 'd'
    elif typekind == TypeKind.Bool:
        return '?'
    elif typekind in [TypeKind.String, TypeKind.Data, TypeKind.Array, TypeKind.Map]:
        return 'I'
    elif typekind == TypeKind.DataFixed:
        return '{}s'.format(length)
    elif typekind == TypeKind.Optional:
        return '?'
    elif typekind == TypeKind.ArrayFixed:
        return ''


def _gen_type(type):
    if isinstance(type, BarePrimitive):
        result = '\t_ast = {}\n\n'.format(type.code())
        result += '\tdef __init__(self, value=None):\n'
        result += '\t\tself.value = value\n\n'
        result += '\tdef pack(self):\n'
        result += '\t\treturn bare.pack(self.value)\n\n'
        result += '\tdef unpack(self, data):\n'
        result += '\t\tself.value = bare.unpack(self, data)\n\n'
        result += '\n'
        return result

    if isinstance(type, StructType):
        result = '\t_ast = {}\n\n'.format(type.code())
        result += '\tdef __init__(self):\n'
        for name in type.fields:
            result += "\t\t{} = None\n".format(name)
        result += "\n"
        result += '\tdef pack(self):\n'
        result += '\t\treturn bare.pack(self)\n\n'
        result += '\tdef unpack(self, data):\n'
        result += '\t\treturn bare.unpack(self, data)\n\n'
        result += '\n'
        return result

    return '\t\tpass\n'


def codegen(schema, output, indent, skip=None):
    if skip is None:
        skip = []
    result = 'from collections import OrderedDict\n\n'
    result += 'import bare\n'
    result += 'from bare.ast import TypeKind, BarePrimitive, StructType, NamedType, ArrayType, MapType\n\n\n'

    schema = bare.parser.parse(schema)

    for type in schema:
        if type.name in skip:
            continue

        if isinstance(type, BareType):
            result += 'class {}:\n'.format(type.name)
            result += _gen_type(type.type)

    if indent != '\t':
        result = result.replace('\t', indent)
    output.write(result)


def main():
    parser = argparse.ArgumentParser(description="BARE Codegen utility")
    parser.add_argument('schema', type=open)
    parser.add_argument('output', type=argparse.FileType('w'))
    parser.add_argument('--skip', '-s', action='append')
    parser.add_argument('--indent', '-i', default='\t')
    args = parser.parse_args()
    codegen(args.schema.read(), args.output, args.indent, args.skip)


if __name__ == '__main__':
    main()
