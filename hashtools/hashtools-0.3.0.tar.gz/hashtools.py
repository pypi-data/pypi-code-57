# -*- coding: utf-8
from __future__ import print_function
from io import open
import os
import sys
import hashlib
import click
import base64

BUFFER_SIZE = 1024 * 64

def get_hash_generator(generator):
    if isinstance(generator, str):
        return hashlib.new(generator)
    else:
        return generator

def update(generator, stream):
    while True:
        buffer = stream.read(BUFFER_SIZE)
        if buffer:
            generator.update(buffer)
        else:
            break
    return generator

def get_raw_stdin():
    stdin = sys.stdin
    if hasattr(stdin, "buffer"):
        return stdin.buffer
    else:
        if os.name == "nt":
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        return stdin

def get_hash_result(generator, result_format, length=None):
    """Choices of result_format are: generator, hex, base64 or bytes(or anything else).
    generator: returns hash generator.
    hex: returns hexlified hash result.
    base: returns base64 encoded hash result.
    bytes: returns raw bytes hash result.
    """
    if result_format == "generator":
        return generator
    elif result_format == "hex":
        try:
            return generator.hexdigest()
        except TypeError:
            return generator.hexdigest(length)
    elif result_format == "base64":
        try:
            data = generator.digest()
        except:
            data = generator.digest(length)
        return "".join(base64.encodebytes(data).strip().decode().splitlines())
    else:
        try:
            return generator.digest()
        except TypeError:
            return generator.digest(length)

def get_file_hash(generator, filename, result_format="hex", length=None):
    generator = get_hash_generator(generator)
    if filename == "-":
        stream = get_raw_stdin()
        generator = update(generator, stream)
    else:
        with open(filename, "rb") as stream:
            generator = update(generator, stream)
    return get_hash_result(generator, result_format, length)

def get_files_hash(generator, filenames, result_format="hex", length=None):
    generator = get_hash_generator(generator)
    for filename in filenames:
        generator = get_file_hash(generator, filename, result_format="generator")
    return get_hash_result(generator, result_format, length)

def get_hash(generator, data, result_format="hex", length=None, encoding="utf-8"):
    if isinstance(data, str):
        data = data.encode(encoding)
    generator = get_hash_generator(generator)
    generator.update(data)
    return get_hash_result(generator, result_format, length)

def export_hash_generator(method):
    @click.command()
    @click.option("-v", "--verbose", is_flag=True, help="Show filename or not.")
    @click.option("-c", "--concat", is_flag=True, help="Concat all files to one file, and get only one hash code.")
    @click.option("-l", "--length", type=int, default=1024, help="Output length for SHAKE object.")
    @click.option("-o", "--output", default="hex", type=click.Choice(['hex', 'base64']), help="Output format, default to hexlify.")
    @click.option("-s", "--strip-stdin", is_flag=True, help="Strip data read from stdin.")
    @click.argument("filenames", nargs=-1)
    def generator(verbose, concat, length, filenames, output, strip_stdin):
        if os.name == "nt":
            sign = "*"
        else:
            sign = " "
        if strip_stdin:
            data = get_raw_stdin().read().strip()
            code = get_hash(method, data, result_format=output, length=length)
            if verbose:
                print("{code} {sign}{filename}".format(code=code, sign=sign, filename=filename.replace("\\", "/")))
            else:
                print(code)
        else:
            filenames = "\n".join(filenames).splitlines()
            if not filenames:
                filenames = ["-"]
            if not concat:
                for filename in filenames:
                    code = get_file_hash(method, filename, result_format=output, length=length)
                    if verbose:
                        print("{code} {sign}{filename}".format(code=code, sign=sign, filename=filename.replace("\\", "/")))
                    else:
                        print(code)
            else:
                code = get_files_hash(method, filenames, result_format=output, length=length)
                if verbose:
                    print(code, "{sign}-".format(sign=sign))
                else:
                    print(code)
    return generator

for method in hashlib.algorithms_available:
    method = method.replace("-", "_")
    globals()[method] = export_hash_generator(method)
