import struct
import sys
from enum import EnumMeta

from bare.ast import StructType, BarePrimitive, TypeKind, NamedType, ArrayType, MapType, OptionalType, UnionType


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


def _unpack_varint(data, offset, signed=False):
    i = 0
    shift = 0
    result = 0
    while True:
        byte = data[offset + i]
        if byte < 0x80:
            value = result | byte << shift

            if signed:
                sign = value % 2
                value = value // 2
                if sign:
                    value = -1 * (value + 1)

            return value, offset + i + 1
        result |= (byte & 0x7f) << shift
        shift += 7
        i += 1


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
    elif primitive.type == TypeKind.Void:
        return b''
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
        raise ValueError("Cannot pack {}".format(primitive.type))


def _unpack_primitive(primitive, data, offset):
    if primitive.type == TypeKind.U8:
        return struct.unpack_from('<B', data, offset)[0], offset + 1
    elif primitive.type == TypeKind.U16:
        return struct.unpack_from('<H', data, offset)[0], offset + 2
    elif primitive.type == TypeKind.U32:
        return struct.unpack_from('<I', data, offset)[0], offset + 4
    elif primitive.type == TypeKind.U64:
        return struct.unpack_from('<Q', data, offset)[0], offset + 8
    elif primitive.type == TypeKind.UINT:
        return _unpack_varint(data, offset)
    elif primitive.type == TypeKind.I8:
        return struct.unpack_from('<b', data, offset)[0], offset + 1
    elif primitive.type == TypeKind.I16:
        return struct.unpack_from('<h', data, offset)[0], offset + 2
    elif primitive.type == TypeKind.I32:
        return struct.unpack_from('<i', data, offset)[0], offset + 4
    elif primitive.type == TypeKind.I64:
        return struct.unpack_from('<q', data, offset)[0], offset + 8
    elif primitive.type == TypeKind.INT:
        return _unpack_varint(data, offset, signed=True)
    elif primitive.type == TypeKind.F32:
        return struct.unpack_from('<f', data, offset)[0], offset + 4
    elif primitive.type == TypeKind.F64:
        return struct.unpack_from('<d', data, offset)[0], offset + 8
    elif primitive.type == TypeKind.Bool:
        return struct.unpack_from('<?', data, offset)[0], offset + 1
    elif primitive.type == TypeKind.Void:
        return None, offset
    elif primitive.type == TypeKind.String or primitive.type == TypeKind.Data:
        length, offset = _unpack_varint(data, offset)
        result = struct.unpack_from('<{}s'.format(length), data, offset)[0]
        offset += len(result)
        if primitive.type == TypeKind.String:
            result = result.decode('utf-8')
        return result, offset
    elif primitive.type == TypeKind.DataFixed:
        return struct.unpack_from('<{}s'.format(primitive.length), data, offset)[0], offset + primitive.length
    else:
        raise NotImplementedError("Cannot unpack {}".format(primitive))


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
        if hasattr(data, 'value'):
            data = data.value
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
    elif isinstance(ast_node, UnionType):
        for type in ast_node.types:
            if type.type.name == data.__class__.__name__:
                untagged = _pack_type(type.type, data, module)
                index = type.value
                break
        else:
            raise ValueError("{} is not a member of {}".format(data.__class__.__name__, ast_node))
        tag = bytes()
        tag += _pack_primitive(BarePrimitive(TypeKind.UINT), index)
        return tag + untagged
    else:
        raise NotImplementedError("Packing {} is not implemented yet".format(ast_node))


def _unpack_type(ast_node, instance, module, data, offset):
    if isinstance(ast_node, StructType):
        for fieldname in ast_node.fields:
            value, offset = _unpack_type(ast_node.fields[fieldname], None, module, data, offset)
            if instance is None:
                instance = {}
            if hasattr(instance, fieldname):
                setattr(instance, fieldname, value)
            else:
                instance[fieldname] = value
        return instance, offset
    elif isinstance(ast_node, BarePrimitive):
        return _unpack_primitive(ast_node, data, offset)
    elif isinstance(ast_node, NamedType):
        referenced = getattr(module, ast_node.name)
        if isinstance(referenced, EnumMeta):
            value, offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
            enum = referenced(value)
            return enum, offset
        else:
            instance = referenced()
            instance, offset = _unpack_type(referenced._ast, instance, module, data, offset)
            return instance, offset
    elif isinstance(ast_node, ArrayType):
        if ast_node.length is None:
            length, offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
        else:
            length = ast_node.length

        result = []
        for i in range(0, length):
            value, offset = _unpack_type(ast_node.subtype, None, module, data, offset)
            result.append(value)
        return result, offset
    elif isinstance(ast_node, MapType):
        length, offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
        result = {}
        for i in range(0, length):
            key, offset = _unpack_type(ast_node.keytype, None, module, data, offset)
            value, offset = _unpack_type(ast_node.valuetype, None, module, data, offset)
            result[key] = value
        return result, offset
    elif isinstance(ast_node, OptionalType):
        exists, offset = _unpack_primitive(BarePrimitive(TypeKind.Bool), data, offset)
        value = None
        if exists:
            unpacked = _unpack_type(ast_node.subtype, None, module, data, offset)
            value, offset = unpacked
        return value, offset
    elif isinstance(ast_node, UnionType):
        tag, offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
        for type in ast_node.types:
            if type.value == tag:
                break
        else:
            raise ValueError("Cannot find type for tag {}".format(tag))
        if isinstance(type.type, BarePrimitive):
            return _unpack_primitive(type.type, data, offset)
        return getattr(module, type.type.name).unpack(data, offset=offset)
    else:
        raise NotImplementedError("{} is not implemented for decoding".format(ast_node))


def pack(instance, member=None):
    if member is None:
        ast = instance._ast
        module = sys.modules[instance.__class__.__module__]
        return _pack_type(ast, instance, module)
    else:
        ast = member._ast
        module = sys.modules[member.__class__.__module__]
        untagged = _pack_type(ast, member, module)
        for type in instance._ast.types:
            if type.type.name == member.__class__.__name__:
                index = type.value
                break
        else:
            raise ValueError("{} is not a member of {}".format(member.__class__.__name__, instance.__name__))
        tag = bytes()
        tag += _pack_primitive(BarePrimitive(TypeKind.UINT), index)
        return tag + untagged


def unpack(instance, data, union=False, offset=0, primitive=False):
    if union:
        module = sys.modules[instance.__module__]
        tag, offset = _unpack_primitive(BarePrimitive(TypeKind.UINT), data, offset)
        for type in instance._ast.types:
            if type.value == tag:
                break
        else:
            raise ValueError("Cannot find type for tag {}".format(tag))
        result = getattr(module, type.type.name).unpack(data, offset=offset)
        if isinstance(result, tuple):
            return result[0]
        else:
            return result
    else:
        ast = instance._ast
        module = sys.modules[instance.__class__.__module__]
        if primitive:
            value, offset = _unpack_type(ast, instance, module, data, offset)
            instance.value = value
            return instance, offset
        return _unpack_type(ast, instance, module, data, offset)
