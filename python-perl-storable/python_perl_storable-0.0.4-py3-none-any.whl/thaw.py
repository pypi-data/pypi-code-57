"""
 * Парсит данные в формате perl Storable и возвращает примитивы и объекты Python
"""

RETRIVE_METHOD = []

import struct
from python_perl_storable.exception import PerlStorableException
from python_perl_storable.constants import *


class StorableReader:
    def __init__(self, storable, classes=None, iconv=None):
        self.storable = storable  # буффер с данными
        self.pos = 0  # позиция в данных
        self.aseen = []  # значения распознанные раньше
        self.aclass = []  # классы распознанные раньше
        self.bless = classes or {}  # классы для распознавания
        self.iconv = iconv  # конвертер строк
        self.type = None

    def read_magic(self):
        """ Считывает магическое число """
        use_network_order = self.readUInt8()
        version_major = use_network_order >> 1
        version_minor = self.readUInt8() if version_major > 1 else 0

        if version_major > STORABLE_BIN_MAJOR or \
            version_major == STORABLE_BIN_MAJOR and version_minor > STORABLE_BIN_MINOR:
            raise PerlStorableException(
                'Версия Storable не совпадает: требуется v%i.%i, а данные имеют версию v%i.%i' % (
                    STORABLE_BIN_MAJOR, STORABLE_BIN_MINOR, version_major, version_minor))

        if use_network_order & 0x1:
            return None  # /* OK */

        length_magic = self.readUInt8()
        use_NV_size = 1 if version_major >= 2 or version_minor >= 2 else 0
        buf = self.read(length_magic)

        if buf != BYTEORDER_BYTES:
            raise PerlStorableException('Magic number is not compatible: %s <> %s' 
                % (buf, BYTEORDER_BYTES))

        if self.readInt8() != SIZE_OF_INT:
            raise PerlStorableException('Integer size is not compatible')
        if self.readInt8() != SIZE_OF_LONG:
            raise PerlStorableException('Long integer size is not compatible')
        if self.readInt8() != SIZE_OF_CHAR_PTR:
            raise PerlStorableException('Pointer size is not compatible')
        if use_NV_size:
            if self.readInt8() != SIZE_OF_NV:
                raise PerlStorableException('Double size is not compatible')

    def seen(self, sv):
        """ Сохраняет в aseen извлечённое из буфера значение и возвращает его """
        self.aseen.append(sv)
        return sv

    def retrieve(self):
        """ Считывает структуру рекурсивно """
        index = self.readUInt8()
        fn = RETRIVE_METHOD[index]
        if fn:
            return fn(self)
        self.type = index
        self.retrieve_other()


    def retrieve_object(self):
        tag = self.readInt32BE()
        if tag < 0 or tag >= len(self.aseen):
            raise PerlStorableException('Object #' + tag + ' out of range')
        return self.aseen[tag]

    def retrieve_other(self):
        raise PerlStorableException("Структура Storable повреждена. Обработчик № " + str(self.type))

    def retrieve_byte(self):
        return self.seen(self.readUInt8() - 128)

    def retrieve_integer(self):
        self.pos += SIZE_OF_LONG
        return self.seen(struct.unpack_from("<q", self.storable, self.pos - SIZE_OF_LONG)[0])

    def retrieve_double(self):
        self.pos += SIZE_OF_LONG
        return self.seen(struct.unpack_from("<d", self.storable, self.pos - SIZE_OF_LONG)[0])

    def retrieve_scalar(self):
        size = self.readUInt8()
        return self.seen(self.get_lstring(size))

    def retrieve_lscalar(self):
        size = self.readInt32LE()
        return self.seen(self.get_lstring(size))

    def retrieve_utf8str(self):
        size = self.readUInt8()
        return self.seen(self.read(size).decode('utf8'))

    def retrieve_lutf8str(self):
        size = self.readInt32LE()
        return self.seen(self.read(size).decode('utf8'))

    def retrieve_array(self):
        size = self.readInt32LE()
        array = self.seen([])
        for i in range(0, size):
            array.append(self.retrieve())

        return array

    def retrieve_ref(self):
        """ Аналога ссылки perl-а в Python нет, в Python всё ссылки, поэтому возвращаем значение так """
        return self.seen(self.retrieve())

    def retrieve_hash(self):
        length = self.readInt32LE()
        hash = self.seen({})
        for i in range(0, length):
            value = self.retrieve()
            size = self.readInt32LE()
            key = self.get_lstring(size)
            hash[key] = value

        return hash

    def retrieve_flag_hash(self):
        hash_flags = self.readUInt8()
        length = self.readInt32LE()
        hash = self.seen({})

        for i in range(0, length):
            value = self.retrieve()
            flags = self.readUInt8()
            key = 0

            if flags & SHV_K_ISSV:
                """ XXX you can't set a placeholder with an SV key.
                   Then again, you can't get an SV key.
                   Without messing around beyond what the API is supposed to do.
                """
                key = self.retrieve()
            else:
                size = self.readInt32LE()
                key = self.get_lstring(size, flags & (SHV_K_UTF8 | SHV_K_WASUTF8))

            hash[key] = value

            # if (hash_flags & SHV_RESTRICTED) or (flags & SHV_K_LOCKED):
            #     Object.defineProperty(hash, key, {
            #         value,
            #         writable: false,
            #         configurable: false,
            #         enumerable: true,
            #     })
            # else:
            #     hash[key] = value

        return hash

    def retrieve_weakref(self):
        return self.retrieve_ref()

    def retrieve_undef(self):
        return self.seen(None)

    def retrieve_sv_undef(self):
        return self.seen(None)

    def make_obj(self, sv, classname):
        classname_python = classname.replace('::', '__')

        # делаем класс F одинаковым с классом self.bless[classname]
        # объекты класса F будут "instanceof A"
        a_class = self.bless[classname] if classname in self.bless else type(classname_python, (
        (list if isinstance(sv, list) else object),), {})

        obj = a_class.__new__(a_class)

        # переписываем свойства
        if isinstance(sv, list):
            for v in sv:
                obj.append(v)
        else:
            for key, val in sv.items():
                setattr(obj, key, val)
        return obj

    def retrieve_blessed(self):
        length = self.readUInt8()

        if length & 0x80:
            length = self.readInt32LE()

        classname = self.get_lstring(length)
        self.aclass.append(classname)
        sv = self.retrieve()
        return self.make_obj(sv, classname)

    def retrieve_idx_blessed(self):
        idx = self.readUInt8()
        if idx & 0x80:
            idx = this.readInt32LE()
        if idx<0 or idx>=len(self.aclass):
            raise PerlStorableException("Повреждена структура Storable: битый индекс в aclass: " + idx)
        classname = this.aclass[idx]
        sv = self.retrieve()
        return self.make_obj(sv, classname)

    def retrieve_overloaded(self):
       return self.retrieve_ref()

    def readUInt8(self):
        self.pos += 1
        return struct.unpack_from("B", self.storable, self.pos - 1)[0]

    def readInt32LE(self):
        self.pos += SIZE_OF_INT
        return struct.unpack_from("<i", self.storable, self.pos - SIZE_OF_INT)[0]

    def readInt32BE(self):
        self.pos += SIZE_OF_INT
        return struct.unpack_from(">i", self.storable, self.pos - SIZE_OF_INT)[0]

    def readInt8(self):
        self.pos += 1
        return struct.unpack_from("b", self.storable, self.pos - 1)[0]

    def read(self, length):
        self.pos += length
        return self.storable[self.pos - length: self.pos]

    def get_lstring(self, length, in_utf8=False):
        if length == 0:
            return ''
        s = self.read(length)

        if in_utf8:
            return s.decode('utf8')
        if is_ascii(s):
            return s.decode('ascii')
        if self.iconv:
            return self.iconv(s)
        return s

    def end(self):
        if self.pos != len(self.storable): raise PerlStorableException('Структура не разобрана до конца')


storable_reader_proto = StorableReader.__dict__

RETRIVE_METHOD = [
    storable_reader_proto.get('retrieve_object', None),  # /* SX_OBJECT -- entry unused dynamically */
    storable_reader_proto.get('retrieve_lscalar', None),  # /* SX_LSCALAR */
    storable_reader_proto.get('retrieve_array', None),  # /* SX_ARRAY */
    storable_reader_proto.get('retrieve_hash', None),  # /* SX_HASH */
    storable_reader_proto.get('retrieve_ref', None),  # /* SX_REF */
    storable_reader_proto.get('retrieve_undef', None),  # /* SX_UNDEF */
    storable_reader_proto.get('retrieve_integer', None),  # /* SX_INTEGER */
    storable_reader_proto.get('retrieve_double', None),  # /* SX_DOUBLE */
    storable_reader_proto.get('retrieve_byte', None),  # /* SX_BYTE */
    storable_reader_proto.get('retrieve_netint', None),  # /* SX_NETINT */
    storable_reader_proto.get('retrieve_scalar', None),  # /* SX_SCALAR */
    storable_reader_proto.get('retrieve_tied_array', None),  # /* SX_TIED_ARRAY */
    storable_reader_proto.get('retrieve_tied_hash', None),  # /* SX_TIED_HASH */
    storable_reader_proto.get('retrieve_tied_scalar', None),  # /* SX_TIED_SCALAR */
    storable_reader_proto.get('retrieve_sv_undef', None),  # /* SX_SV_UNDEF */
    storable_reader_proto.get('retrieve_sv_yes', None),  # /* SX_SV_YES */
    storable_reader_proto.get('retrieve_sv_no', None),  # /* SX_SV_NO */
    storable_reader_proto.get('retrieve_blessed', None),  # /* SX_BLESS */
    storable_reader_proto.get('retrieve_idx_blessed', None),  # /* SX_IX_BLESS */
    storable_reader_proto.get('retrieve_hook', None),  # /* SX_HOOK */
    storable_reader_proto.get('retrieve_overloaded', None),  # /* SX_OVERLOAD */
    storable_reader_proto.get('retrieve_tied_key', None),  # /* SX_TIED_KEY */
    storable_reader_proto.get('retrieve_tied_idx', None),  # /* SX_TIED_IDX */
    storable_reader_proto.get('retrieve_utf8str', None),  # /* SX_UTF8STR  */
    storable_reader_proto.get('retrieve_lutf8str', None),  # /* SX_LUTF8STR */
    storable_reader_proto.get('retrieve_flag_hash', None),  # /* SX_FLAG_HASH */
    storable_reader_proto.get('retrieve_code', None),  # /* SX_CODE */
    storable_reader_proto.get('retrieve_weakref', None),  # /* SX_WEAKREF */
    storable_reader_proto.get('retrieve_weakoverloaded', None),  # /* SX_WEAKOVERLOAD */
    storable_reader_proto.get('retrieve_vstring', None),  # /* SX_VSTRING */
    storable_reader_proto.get('retrieve_lvstring', None),  # /* SX_LVSTRING */
    storable_reader_proto.get('retrieve_svundef_elem', None),  # /* SX_SVUNDEF_ELEM */
    storable_reader_proto.get('retrieve_regexp', None),  # /* SX_REGEXP */
    storable_reader_proto.get('retrieve_lobject', None),  # /* SX_LOBJECT */
    storable_reader_proto.get('retrieve_other', None),  # /* SX_LAST */
]


def thaw(storable, classes=None, iconv=None):
    stream = StorableReader(storable, classes, iconv)
    stream.read_magic()
    result = stream.retrieve()
    stream.end()
    return result
