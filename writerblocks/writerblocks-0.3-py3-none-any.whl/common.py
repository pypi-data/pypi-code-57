import os.path
import re

from argparse import Namespace
from copy import copy

INDEX_FNAME_BROAD = re.compile(r'.*index.*\.(ya?ml)|(json)')
INDEX_FNAME_BEST = re.compile(r'index\.(ya?ml)|(json)')

INDEX_FILENAME = 'index.yaml'
FORMAT_FILENAME = 'format.yaml'
CONFIG_FILENAME = 'config.yaml'

INI_FILENAME = 'writerblocks.ini'

DEFAULT_FMT = {'default_sep': '\n\n***\n\n',
               'seps': [],
               'preamble': 'preamble.tex'}

DEFAULT_CONFIG = {'in_fmt': 'markdown',
                  'out_fmt': 'pdf',
                  'out_file': 'example.pdf',
                  'index_file': 'index.yaml',
                  'tags': [],
                  'blacklist_tags': [],
                  'pandoc_args': [],
                  'new_project': False,
                  'all_tags': False
                  }

DEFAULT_OPTIONS = Namespace(base_dir=os.path.abspath(os.path.curdir),
                            fmt=DEFAULT_FMT,
                            **DEFAULT_CONFIG
                            )

options = copy(DEFAULT_OPTIONS)
