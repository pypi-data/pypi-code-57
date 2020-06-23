# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spor', 'spor.alignment', 'spor.repository']

package_data = \
{'': ['*']}

install_requires = \
['docopt_subcommands>=2.3,<3.0', 'exit_codes>=1.1,<2.0', 'pyyaml>=3.13,<4.0']

entry_points = \
{'console_scripts': ['spor = spor.cli:main']}

setup_kwargs = {
    'name': 'spor',
    'version': '1.1.6',
    'description': 'A system for anchoring metadata in external files to source code',
    'long_description': '|Python version| |Build Status|\n\n======\n spor\n======\n\n**NB:** This Python implementation of spor has been superseded by a `Rust\nimplementation <https://github.com/abingham/spor>`_. This version might be\nkept compatible with the Rust version, but don\'t count on it for now.\n\nA system for anchoring metadata in external files to source code.\n\nspor lets you define metadata for elements of your source code. The\nmetadata is kept in a separate file from your source code, meaning that\nyou don\'t need to clutter your source file with extra information\nencoded into comments. To accomplish this while dealing with the fact\nthat source code changes over time, spor uses various "anchoring"\ntechniques to keep the metadata in sync with the source code (or let you\nknow when they become unmanageably out of sync).\n\nQuickstart\n==========\n\nBefore you can use spor to anchor metadata to files, you need to initialize a\nrepository with the ``init`` command::\n\n  $ spor init\n\nThis is very similar in spirit to ``git init``. It creates a new directory in your\ncurrent directory called ``.spor``, and this is where spor will keep the\ninformation it needs.\n\nNow you can create anchors. Suppose you\'ve got a file, ``example.py``, like\nthis:\n\n.. code-block:: python\n\n   # example.py\n\n\n   def func(x):\n       return x * 2\n\nYou can anchor metadata to line 4 (the function definition) by specifying the starting offset and anchor width like this::\n\n  $ echo "{\\"meta\\": \\"data\\"}" | spor add example.py 32 12 10\n\n.. pull-quote::\n\n  You don\'t have to pipe the metadata into the ``add`` command. If you don\'t,\n  spor will pop up an editor so that you can enter the metadata there.\n\nThe `10` at the end specifies the size of the "context" around the anchored code\nthat we use for updating anchors.\n\nThis will associate the dictionary ``{meta: data}`` with the code `return x * 2`. You can see\nthis metadata by using the ``list`` command::\n\n  $ spor list example.py\n  example.py:32 => {\'meta\': \'data\'}\n\nThe metadata can be any valid JSON. spor doesn\'t look at the data at all, so\nit\'s entirely up to you to decide what goes there.\n\nMotivation\n==========\n\nMy main motivation for this tool comes from my work on the mutation\ntesting tool `Cosmic Ray <https://github.com/sixty-north/cosmic-ray>`__.\nCR users need to be able to specify sections of their source code which\nshould not be mutated, or which should only be mutated in specific ways.\nRather than having them embed these processing directives in the source\ncode, I thought it would be cleaner and neater to let them do so with a\nseparate metadata file.\n\nFeatures\n========\n\nspor needs support for the following functionality:\n\n1. Add/edit/delete metadata to a specific range of text in a source file\n2. Query existing metadata\n3. Automatically update metadata when possible, or report errors when\n   not\n4. Provide facilities facilities for "updating" metadata with new\n   anchoring data\n\nThe design needs to be sensitive to both human users (i.e. since they\nmay need to manually work with the metadata from time to time) as well\nas programmatic users. I\'m sure the design will evolve as we go, so I\'m\ngoing to try to keep it simple and explicit at first.\n\nIdeally spor will work on any programming language (and, really, any\ntext document), though its initial target will be Python source code.\n\nDevelopment\n===========\n\nSpor is new and small enough that we do fun things like try out new tools.\nInstead of `setuptools` et al., we\'re using `poetry\n<https://github.com/sdispater/poetry>`__. So if you want to contribute to spor,\nthe first thing you need to do is to `install poetry\n<https://github.com/sdispater/poetry#installation>`__.\n\nTo install the package, use::\n\n  poetry install\n\nTests\n-----\n\nThe installation command above will install all of the test dependencies as\nwell. To run all of the tests, run |tox|_:\n\n.. code-block::\n\n  tox\n\nTo run just the `pytests` unit tests, run::\n\n  poetry run pytest tests/unittests\n\nTo run the `radish` tests, run::\n\n  poetry run radish tests/e2e/features -b tests/e2e/radish\n\nNotes\n=====\n\nThe field of "anchoring" is not new, and there\'s some existing work we\nneed to pay attention to:\n\n- Bielikova, Maria. `"Metadata Anchoring for Source Code: Robust Location Descriptor Definition, Building and Interpreting" <https://www.researchgate.net/profile/Maria\\_Bielikova/publication/259892218\\_Metadata\\_Anchoring\\_for\\_Source\\_Code\\_Robust\\_Location\\_Descriptor\\_Definition\\_Building\\_and\\_Interpreting/links/560478cb08aeb5718ff00039.pdf>`__\n\n.. |Python version| image:: https://img.shields.io/badge/Python_version-3.4+-blue.svg\n   :target: https://www.python.org/\n.. |Build Status| image:: https://travis-ci.org/abingham/spor.png?branch=master\n   :target: https://travis-ci.org/abingham/spor\n.. |tox| replace:: ``tox``\n.. _tox: https://tox.readthedocs.io/en/latest/\n',
    'author': 'Austin Bingham',
    'author_email': 'austin@sixty-north.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abingham/spor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
