# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.simple_footnotes']

package_data = \
{'': ['*']}

install_requires = \
['html5lib>=1.0,<2.0', 'pelican>=4.2,<5.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-simple-footnotes',
    'version': '1.0.1',
    'description': 'Pelican plugin to add footnotes to articles and pages',
    'long_description': 'Simple Footnotes\n================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/simple-footnotes/build)](https://github.com/pelican-plugins/simple-footnotes/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-simple-footnotes)](https://pypi.org/project/pelican-simple-footnotes/)\n\nSimple Footnotes is a Pelican plugin for adding footnotes to articles and pages.\n\nInstallation\n------------\n\nThis plugin, and its dependent package `html5lib`, can be installed via:\n\n    python -m pip install pelican-simple-footnotes\n\nUsage\n-----\n\nWhen writing an article or page, add a footnote like this:\n\n    Here’s my written text[ref]and here is a footnote[/ref].\n\nThis will appear as, roughly:\n\nHere’s my written text<sup>1</sup>\n\n 1. and here is a footnote ↩\n\nThis should work with any content format (reST, Markdown, et cetera), because\nit looks for `[ref]` and `[/ref]` once the conversion to HTML has happened.\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\nCredits\n-------\n\nOriginally authored by [Stuart Langridge](https://kryogenix.org/), February 2014,\nand subsequently enhanced by members of the Pelican community, including\n[Justin Mayer](https://justinmayer.com/), who re-packaged it for publication to\nPyPI.\n\nInspired by Andrew Nacin’s [Simple Footnotes WordPress plugin](https://wordpress.org/plugins/simple-footnotes/).\n\n\n[existing issues]: https://github.com/pelican-plugins/simple-footnotes/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'Stuart Langridge',
    'author_email': 'sil@kryogenix.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/simple-footnotes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
