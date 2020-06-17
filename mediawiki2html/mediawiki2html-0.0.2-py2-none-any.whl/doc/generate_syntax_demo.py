from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from mediawiki import *
from io import open
import six

source = ''
with open("syntax") as f:
    for line in f:
        source += line

wiki_content = wiki2html(source, True)
output_fn = six.ensure_binary if six.PY2 else six.ensure_text
print(output_fn(wiki_content))
