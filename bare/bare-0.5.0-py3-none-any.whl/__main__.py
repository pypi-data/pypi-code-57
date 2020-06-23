import argparse
import bare.parser
from bare.ast import BareType, BarePrimitive, StructType, TypeKind, BareEnum, UnionType


def _gen_enum(type):
    result = ""
    for ev in type.values:
        result += '\t{} = {}\n'.format(ev.name, ev.value)
    result += "\n\n"
    return result


def _gen_type(type):
    if isinstance(type, BarePrimitive):
        result = '\t_ast = {}\n\n'.format(type.code())
        result += '\tdef __init__(self, value=None):\n'
        result += '\t\tself.value = value\n\n'
        result += '\tdef pack(self):\n'
        result += '\t\treturn bare.pack(self)\n\n'
        result += '\t@classmethod\n'
        result += '\tdef unpack(cls, data, offset=0):\n'
        result += '\t\tinstance = cls()\n'
        result += '\t\treturn bare.unpack(instance, data, offset=offset, primitive=True)\n\n'
        result += '\n'
        return result

    if isinstance(type, StructType):
        result = '\t_ast = {}\n\n'.format(type.code())
        result += '\tdef __init__(self):\n'
        for name in type.fields:
            result += "\t\tself.{} = None\n".format(name)
        result += "\n"
        result += '\tdef pack(self):\n'
        result += '\t\treturn bare.pack(self)\n\n'
        result += '\t@classmethod\n'
        result += '\tdef unpack(cls, data, offset=0):\n'
        result += '\t\tinstance = cls()\n'
        result += '\t\tbare.unpack(instance, data, offset=offset)\n'
        result += '\t\treturn instance\n\n'
        result += '\n'
        return result

    if isinstance(type, UnionType):
        result = '\t_ast = {}\n\n'.format(type.code())
        result += '\t@classmethod\n'
        result += '\tdef pack(cls, member):\n'
        result += '\t\treturn bare.pack(cls, member)\n\n'
        result += '\t@classmethod\n'
        result += '\tdef unpack(cls, data, offset=0):\n'
        result += '\t\treturn bare.unpack(cls, data, union=True, offset=offset)\n\n'
        result += '\n'
        return result

    raise NotImplementedError("Cannot codegen {}".format(type))


def codegen(schema, output, indent, skip=None):
    if skip is None:
        skip = []
    result = 'from collections import OrderedDict\n'
    result += 'from enum import Enum\n\n'
    result += 'import bare\n'
    result += 'from bare.ast import TypeKind, BarePrimitive, StructType, OptionalType, NamedType, ArrayType, MapType, UnionType, UnionValue\n\n\n'

    schema = bare.parser.parse(schema)

    for type in schema:
        if type.name in skip:
            continue

        if isinstance(type, BareType):
            result += 'class {}:\n'.format(type.name)
            result += _gen_type(type.type)
        if isinstance(type, BareEnum):
            result += 'class {}(Enum):\n'.format(type.name)
            result += _gen_enum(type)

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
