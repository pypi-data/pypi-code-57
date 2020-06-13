# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'holo',
    'version': '0.1.3',
    'description': 'Holo is a library provides overload like cpp',
    'long_description': '# holo\nHolo is a library provides overload like cpp\n\n## Installation\n\n```py\npip install holo\n```\n\n\n## A Simple Example\n\n```py\nfrom holo import overload\n\n@overload\ndef add(l, r):\n    return l + r\n\n@overload\ndef add(l):\n    return l + 2\n\nadd(3)\n#>5\nadd(3, 4)\n#>7\n\nclass Foo:\n    def __init__(self, l):\n        self.l = l\n\n    @overload\n    def add(self):\n        return self.l + 2\n\n    @overload\n    def add(self, r):\n        return self.l + r\n\nf = Foo(3)\nf.add()\n#>5\nf.add(4)\n#>7\n```',
    'author': 'lvzhi',
    'author_email': '279094354@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Na0ture/holo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
