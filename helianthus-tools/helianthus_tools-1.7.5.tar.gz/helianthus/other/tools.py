# -*- coding: UTF-8 -*-
import os

def f2x(filepath) -> str:
    result = ""
    with open(filepath, "rb") as f:
        for _ in range(os.path.getsize(filepath)):
            item = str(hex(ord(f.read(1))))
            item = r"\x" + item[2:].rjust(2, "0").upper()
            result += item
    return result

def reverse_shellcode(shellcode) -> None:
    shellcode_lenght = len(shellcode)
    print("int buf[%d] = {" %shellcode_lenght)
    for index, i in enumerate(shellcode[::-1]):
        print("0x" + str(hex(ord(i)))[2:].rjust(2, "0").upper(), end=", ")
        index += 1
        if index % 7 == 0:
            print()
    print()
    print("};")