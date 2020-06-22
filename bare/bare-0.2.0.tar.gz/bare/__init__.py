import struct
import sys
from enum import EnumMeta

from bare.ast import StructType, BarePrimitive, TypeKind, NamedType, ArrayType, MapType, OptionalType


def _pack_varint(data, signed=False):
    result = bytes()
    if signed:
        if data < 0:
            data = (2 * abs(data)) - 1
        else:
            data = 2 * data
    while data >= 0x80:
        result += struct.pack('<B', (data & 0xff) | 0x80)
        data >>= 7
    result += struct.pack('<B', data)
    return result


def _pack_primitive(primitive, data):
    if primitive.type == TypeKind.U8:
        return struct.pack('<B', data)
    elif primitive.type == TypeKind.U16:
        return struct.pack('<H', data)
    elif primitive.type == TypeKind.U32:
        return struct.pack('<I', data)
    elif primitive.type == TypeKind.U64:
        return struct.pack('<Q', data)
    elif primitive.type == TypeKind.UINT:
        return _pack_varint(data)
    elif primitive.type == TypeKind.I8:
        return struct.pack('<b', data)
    elif primitive.type == TypeKind.I16:
        return struct.pack('<h', data)
    elif primitive.type == TypeKind.I32:
        return struct.pack('<i', data)
    elif primitive.type == TypeKind.I64:
        return struct.pack('<q', data)
    elif primitive.type == TypeKind.INT:
        return _pack_varint(data, signed=True)
    elif primitive.type == TypeKind.F32:
        return struct.pack('<f', data)
    elif primitive.type == TypeKind.F64:
        return struct.pack('<d', data)
    elif primitive.type == TypeKind.Bool:
        return struct.pack('<?', data)
    elif primitive.type == TypeKind.String or primitive.type == TypeKind.Data:
        if primitive.type == TypeKind.String:
            data = data.encode('utf-8')
        length = len(data)
        result = bytes()
        result += _pack_primitive(BarePrimitive(TypeKind.UINT), length)
        result += struct.pack('<{}s'.format(length), data)
        return result
    elif primitive.type == TypeKind.DataFixed:
        return struct.pack('<{}s'.format(primitive.length), data)
    else:
        raise ValueError("oops")


def _pack_type(ast_node, data, module):
    if not isinstance(ast_node, OptionalType) and data is None:
        raise ValueError("Value is required")

    if isinstance(ast_node, StructType):
        result = bytes()
        for fieldname in ast_node.fields:
            if hasattr(data, fieldname):
                subdata = getattr(data, fieldname)
            elif fieldname in data:
                subdata = data[fieldname]
            else:
                raise ValueError("Could not vind a value for {}".format(fieldname))
            result += _pack_type(ast_node.fields[fieldname], subdata, module)
        return result
    elif isinstance(ast_node, BarePrimitive):
        return _pack_primitive(ast_node, data)
    elif isinstance(ast_node, NamedType):
        referenced = getattr(module, ast_node.name)
        if isinstance(referenced, EnumMeta):
            return _pack_type(BarePrimitive(TypeKind.UINT), data.value, module)
        else:
            return _pack_type(referenced._ast, data, module)
    elif isinstance(ast_node, ArrayType):
        result = bytes()
        if ast_node.length is None:
            result += _pack_primitive(BarePrimitive(TypeKind.UINT), len(data))
        elif len(data) != ast_node.length:
            raise ValueError("Unexpected number of values, expected {}, got {}".format(ast_node.length, len(data)))
        for item in data:
            result += _pack_type(ast_node.subtype, item, module)
        return result
    elif isinstance(ast_node, MapType):
        result = bytes()
        result += _pack_primitive(BarePrimitive(TypeKind.UINT), len(data))
        for key in data:
            result += _pack_type(ast_node.keytype, key, module)
            result += _pack_type(ast_node.valuetype, data[key], module)
        return result
    elif isinstance(ast_node, OptionalType):
        result = _pack_primitive(BarePrimitive(TypeKind.Bool), data is not None)
        if data is not None:
            result += _pack_type(ast_node.subtype, data, module)
        return result
    else:
        raise ValueError("Don't know how to pack this yet")


def pack(instance, member=None):
    if member is None:
        ast = instance._ast
        module = sys.modules[instance.__class__.__module__]
        return _pack_type(ast, instance, module)
    else:
        ast = member._ast
        module = sys.modules[member.__class__.__module__]
        untagged = _pack_type(ast, member, module)
        index = 0
        for type in instance._ast.types:
            if type.name == member.__class__.__name__:
                break
            index += 1
        else:
            raise ValueError("{} is not a member of {}".format(member.__class__.__name__, instance.__name__))
        tag = bytes()
        tag += _pack_primitive(BarePrimitive(TypeKind.UINT), index)
        return tag + untagged


def unpack(instance, data, member=None):
    ast = instance._ast
