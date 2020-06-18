import re
import os

CLANG_FORMAT_VERSION = '8'
YAPF_VERSION = '0.24.0'
FORMATTABLE_LANGUAGES = ['c', 'py']
CHECKED_FILES = re.compile(
    r'.*(\.(i?[ch](pp|xx|c)?|cc|hh|py|C|cmake|[yx]ml|qm[ts]|dtd|xsd|ent|bat|[cz]?sh|js|html?)|'
    r'CMakeLists.txt|Jenkinsfile)$')

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
