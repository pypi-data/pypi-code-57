import os
from pathlib import Path
import re

file_path = Path(Path(os.getcwd()).parent, 'v5automation', 'generated', 'interfaces')


# temp_file = 'axis_system.py'

def regex_file(temp_file):
    with open(temp_file, '+r') as file:
        org_contents = file.read()

        regex_1 = re.compile(r' {16}\|{1}\n\n')
        contents = regex_1.sub('\n', org_contents)

        regex_2 = re.compile(r'Example: ')
        contents = regex_2.sub('\n                |\n                | Example:\n                | ', contents)

        regex_3 = re.compile(r'\n\n( ){16}\|( ){16}')
        contents = regex_3.sub('\n                |\n                ', contents)

        regex_3 = re.compile(r'\n( ){16}(\|)\n( ){8}:param')
        contents = regex_3.sub('\n        :param', contents)

        if org_contents == contents:
            print('no change')

        file.seek(0)
        file.write(contents)
        file.truncate()


print(file_path)
files = file_path.rglob("*.py")
for file in files:
    print(f'processing file: {file}')
    regex_file(file)
