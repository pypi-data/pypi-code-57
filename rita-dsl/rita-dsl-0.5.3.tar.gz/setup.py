# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rita', 'rita.engine', 'rita.modules']

package_data = \
{'': ['*']}

install_requires = \
['ply==3.11']

entry_points = \
{'console_scripts': ['rita = rita.run:main']}

setup_kwargs = {
    'name': 'rita-dsl',
    'version': '0.5.3',
    'description': 'DSL for building language rules',
    'long_description': '# RITA DSL\n\n[![Documentation Status](https://readthedocs.org/projects/rita-dsl/badge/?version=latest)](http://rita-dsl.readthedocs.io/?badge=latest)\n[![codecov](https://codecov.io/gh/zaibacu/rita-dsl/branch/master/graph/badge.svg)](https://codecov.io/gh/zaibacu/rita-dsl)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/zaibacu/rita-dsl/graphs/commit-activity)\n[![PyPI version fury.io](https://badge.fury.io/py/rita-dsl.svg)](https://pypi.python.org/pypi/rita-dsl/)\n[![PyPI download month](https://img.shields.io/pypi/dm/rita-dsl.svg)](https://pypi.python.org/pypi/rita-dsl/)\n[![GitHub license](https://img.shields.io/github/license/zaibacu/rita-dsl.svg)](https://github.com/zaibacu/rita-dsl/blob/master/LICENSE)\n\nThis is a language, loosely based on language [Apache UIMA RUTA](https://uima.apache.org/ruta.html), focused on writing manual language rules, which compiles into either [spaCy](https://github.com/explosion/spaCy) compatible patterns, or pure regex. These patterns can be used for doing [manual NER](https://spacy.io/api/entityruler) as well as used in other processes, like retokenizing and pure matching\n\n## An Introduction Video\n[![Intro](https://img.youtube.com/vi/GScerMeWz68/0.jpg)](https://www.youtube.com/watch?v=GScerMeWz68)\n\n## Links\n- [Live Demo](https://rita-demo.herokuapp.com/)\n- [Documentation](http://rita-dsl.readthedocs.io/)\n- [QuickStart](https://rita-dsl.readthedocs.io/en/latest/quickstart/)\n\n## Support\n\n[![reddit](https://img.shields.io/reddit/subreddit-subscribers/ritaDSL?style=social)](https://www.reddit.com/r/ritaDSL/)\n[![Gitter](https://badges.gitter.im/rita-dsl/community.svg)](https://gitter.im/rita-dsl/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n\n## Install\n\n`pip install rita-dsl`\n\n## Simple Rules example\n\n```python\nrules = """\ncuts = {"fitted", "wide-cut"}\nlengths = {"short", "long", "calf-length", "knee-length"}\nfabric_types = {"soft", "airy", "crinkled"}\nfabrics = {"velour", "chiffon", "knit", "woven", "stretch"}\n\n{IN_LIST(cuts)?, IN_LIST(lengths), WORD("dress")}->MARK("DRESS_TYPE")\n{IN_LIST(lengths), IN_LIST(cuts), WORD("dress")}->MARK("DRESS_TYPE")\n{IN_LIST(fabric_types)?, IN_LIST(fabrics)}->MARK("DRESS_FABRIC")\n"""\n```\n\n### Loading in spaCy\n```python\nimport spacy\nfrom rita.shortcuts import setup_spacy\n\n\nnlp = spacy.load("en")\nsetup_spacy(nlp, rules_string=rules)\n```\n\nAnd using it:\n```python\n>>> r = nlp("She was wearing a short wide-cut dress")\n>>> [{"label": e.label_, "text": e.text} for e in r.ents]\n[{\'label\': \'DRESS_TYPE\', \'text\': \'short wide-cut dress\'}]\n```\n\n### Loading using Regex (standalone)\n```python\nimport rita\n\npatterns = rita.compile_string(rules, use_engine="standalone")\n```\n\nAnd using it:\n```python\n>>> list(patterns.execute("She was wearing a short wide-cut dress"))\n[{\'end\': 38, \'label\': \'DRESS_TYPE\', \'start\': 18, \'text\': \'short wide-cut dress\'}]\n```\n\n## Special Thank You\n\nSpecial thanks goes to \n\n[![JetBrains](docs/assets/jetbrains.svg?raw=true)](https://www.jetbrains.com/?from=rita-dsl)\n\nfor supporting development of this library\n',
    'author': 'Šarūnas Navickas',
    'author_email': 'zaibacu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zaibacu/rita-dsl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
