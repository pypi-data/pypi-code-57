import json
from os import path
import pyperclip

def lookup(code1, code2):
    codes_filename = path.join(path.expanduser("~"),'.ibsec_codes.json')
    with open(codes_filename) as codes_file:
        CODES = json.load(codes_file)
    response = CODES[code1 - 1] + CODES[code2 - 1]
    pyperclip.copy(response)
    print (response + ' has been copied to the clipboard!')

