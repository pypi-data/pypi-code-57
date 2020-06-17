import os
from cffi import FFI

__dir__ = os.path.dirname(os.path.abspath(__file__))

lib = os.path.join(__dir__, "..", "lib")
lrt = os.path.join(lib, "runtime.so")
header = os.path.join(lib, "runtime.h")

ffi = FFI()

ffi.set_source(
    '_runtime',
    '#include <runtime.h>',
    include_dirs=[lib],
    extra_objects=[lrt],
)

with open(header, 'r') as f:
    ffi.cdef(f.read())


if __name__ == '__main__':
    ffi.compile()
