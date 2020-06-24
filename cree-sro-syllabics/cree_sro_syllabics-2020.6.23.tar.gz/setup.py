# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cree_sro_syllabics']
setup_kwargs = {
    'name': 'cree-sro-syllabics',
    'version': '2020.6.23',
    'description': 'Convert between Western Cree SRO and syllabics',
    'long_description': 'Cree SRO/Syllabics\n==================\n\n[![Build Status](https://travis-ci.org/eddieantonio/cree-sro-syllabics.svg?branch=master)](https://travis-ci.org/eddieantonio/cree-sro-syllabics)\n[![codecov](https://codecov.io/gh/eddieantonio/cree-sro-syllabics/branch/master/graph/badge.svg)](https://codecov.io/gh/eddieantonio/cree-sro-syllabics)\n[![Documentation Status](https://readthedocs.org/projects/crk-orthography/badge/?version=stable)](https://crk-orthography.readthedocs.io/en/stable/?badge=stable)\n[![PyPI package](https://img.shields.io/pypi/v/cree-sro-syllabics.svg)](https://pypi.org/project/cree-sro-syllabics/)\n[![Calver YYYY.MM.DD](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg)](http://calver.org/)\n\nPython 3 library to convert between Western Cree **standard Roman\nOrthography** (SRO) to **syllabics** and back again!\n\nCan be used for:\n\n - nêhiyawêwin/ᓀᐦᐃᔭᐍᐏᐣ/Cree Y-dialect\n - nīhithawīwin/ᓃᐦᐃᖬᐑᐏᐣ/Cree Th-dialect\n - nēhinawēwin/ᓀᐦᐃᓇᐍᐏᐣ/Cree N-dialect\n\nInstall\n-------\n\nUsing `pip`:\n\n    pip install cree-sro-syllabics\n\nOr, you can copy-paste or download [`cree_sro_syllabics.py`][download] into\nyour own Python 3 project!\n\n[download]: https://github.com/eddieantonio/cree-sro-syllabics/raw/master/cree_sro_syllabics.py\n\n\nUsage\n-----\n\n[Visit the full documentation here][documentation]! Wondering about\nwords like "syllabics", "transliterator", or "orthography"? Visit\n[the glossary][glossary]!\n\n[documentation]: https://crk-orthography.readthedocs.io/en/stable/\n[glossary]: https://crk-orthography.readthedocs.io/en/stable/glossary.html\n\n\nConvert SRO to syllabics:\n\n```python\n>>> from cree_sro_syllabics import sro2syllabics\n>>> sro2syllabics(\'nêhiyawêwin\')\n\'ᓀᐦᔭᐍᐏᐣ\'\n>>> sro2syllabics(\'write nêhiyawêwin\')\n\'write ᓀᐦᐃᔭᐍᐏᐣ\'\n```\n\nConvert syllabics to SRO:\n\n```python\n>>> from cree_sro_syllabics import syllabics2sro\n>>> syllabics2sro(\'ᐊᒋᒧᓯᐢ\')\n\'acimosis\'\n>>> syllabics2sro(\' → ᒪᐢᑫᑯᓯᕽ  ᑎᕒᐁᕀᓬ \')\n\' → maskêkosihk  tireyl \'\n```\n\nSee also\n--------\n\n[nêhiyawêwin syllabics](https://github.com/UAlbertaALTLab/nehiyawewin-syllabics)\n\n\nLicense\n-------\n\nCopyright (C) 2018 Eddie Antonio Santos\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as\npublished by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Eddie Antonio Santos',
    'author_email': 'easantos@ualberta.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eddieantonio/cree-sro-syllabics',
    'py_modules': modules,
}


setup(**setup_kwargs)
