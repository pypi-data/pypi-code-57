# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_revealjs', 'sphinx_revealjs.themes']

package_data = \
{'': ['*'],
 'sphinx_revealjs.themes': ['sphinx_revealjs/*',
                            'sphinx_revealjs/static/revealjs/*',
                            'sphinx_revealjs/static/revealjs/css/*',
                            'sphinx_revealjs/static/revealjs/css/print/*',
                            'sphinx_revealjs/static/revealjs/css/theme/*',
                            'sphinx_revealjs/static/revealjs/css/theme/source/*',
                            'sphinx_revealjs/static/revealjs/css/theme/template/*',
                            'sphinx_revealjs/static/revealjs/js/*',
                            'sphinx_revealjs/static/revealjs/lib/css/zenburn.css',
                            'sphinx_revealjs/static/revealjs/lib/font/league-gothic/*',
                            'sphinx_revealjs/static/revealjs/lib/font/source-sans-pro/*',
                            'sphinx_revealjs/static/revealjs/lib/js/html5shiv.js',
                            'sphinx_revealjs/static/revealjs/plugin/highlight/*',
                            'sphinx_revealjs/static/revealjs/plugin/markdown/*',
                            'sphinx_revealjs/static/revealjs/plugin/math/*',
                            'sphinx_revealjs/static/revealjs/plugin/multiplex/*',
                            'sphinx_revealjs/static/revealjs/plugin/notes-server/*',
                            'sphinx_revealjs/static/revealjs/plugin/notes/*',
                            'sphinx_revealjs/static/revealjs/plugin/print-pdf/*',
                            'sphinx_revealjs/static/revealjs/plugin/search/*',
                            'sphinx_revealjs/static/revealjs/plugin/zoom-js/*']}

install_requires = \
['docutils', 'sphinx']

setup_kwargs = {
    'name': 'sphinx-revealjs',
    'version': '0.12.0',
    'description': 'Sphinx extension with theme to generate Reveal.js presentation',
    'long_description': "sphinx-revealjs\n===============\n\n.. image:: https://img.shields.io/pypi/v/sphinx-revealjs.svg\n    :target: https://pypi.org/project/sphinx-revealjs/\n\n.. image:: https://github.com/attakei/sphinx-revealjs/workflows/Testings/badge.svg\n    :target: https://github.com/attakei/sphinx-revealjs/actions\n\n.. image:: https://travis-ci.org/attakei/sphinx-revealjs.svg?branch=master\n    :target: https://travis-ci.org/attakei/sphinx-revealjs\n\n\nSphinx extention with theme to generate Reveal.js presentation\n\nOrverview\n---------\n\nThis extension generate Reveal.js presentation\nfrom **standard** reStructuredText.\n\nIt include theses features.\n\n* Custom builder to translate from reST to reveal.js style HTML\n* Template to be enable to render presentation local imdependent\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ pip install sphinx-revealjs\n\n\nUsage\n-----\n\n1. Create your sphinx documentation\n2. Edit `conf.py` to use this extension\n\n    .. code-block:: python\n\n        extensions = [\n            'sphinx_revealjs',\n        ]\n\n3. Write source for standard document style\n\n4. Build sources as Reveal.js presentation\n\n    .. code-block:: bash\n\n        $ make revealjs\n\nChange logs\n-----------\n\nSee `it <./CHANGES.rst>`_\n\nFutures\n-------\n\n* Index template as none presentation\n* CDN support\n\n\nCopyright\n---------\n\nApache-2.0 license. Please see `LICENSE <./LICENSE>`_.\n",
    'author': 'Kazuya Takei',
    'author_email': 'myself@attakei.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/attakei/sphinx-revealjs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
