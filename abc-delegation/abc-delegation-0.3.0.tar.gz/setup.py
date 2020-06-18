# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abc_delegation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'abc-delegation',
    'version': '0.3.0',
    'description': 'A tool for automated delegation with abstract base classes',
    'long_description': '# abc-delegation\n\n[![Codeship Status for monomonedula/abc-delegation](https://app.codeship.com/projects/5be7b410-92cb-0138-678c-1680fac8559a/status?branch=master)](https://app.codeship.com/projects/400234)\n[![codecov](https://codecov.io/gh/monomonedula/abc-delegation/branch/master/graph/badge.svg)](https://codecov.io/gh/monomonedula/abc-delegation)\n[![PyPI version](https://badge.fury.io/py/abc-delegation.svg)](https://badge.fury.io/py/abc-delegation)\n\nA tool for automated delegation with abstract base classes.\n\nThis metaclass enables creation of delegating classes \ninheriting from an abstract base class. \n\nThis technique is impossible with regular `__getattr__` approach for delegation,\nso normally, you would have to define every delegated method explicitly.\nNot any more\n\nThe metaclasses also enable optional validation of the delegate attributes\nto ensure they have all of the methods required by the parent object.\n\n### Installation:\n`pip install abc-delegation`\n\n\n### Basic usage:\n```python    \nfrom abc import ABCMeta\n\nfrom abc_delegation import delegation_metaclass\n\nclass A(metaclass=ABCMeta):\n    @abstractmethod\n    def bar(self):\n        pass\n\n    @abstractmethod\n    def foo(self):\n        pass\n\nclass B:\n    def bar(self):\n        return "B bar"\n\n    def foo(self):\n        return "B foo"\n\nclass C(A, metaclass=delegation_metaclass("my_delegate")):\n    def __init__(self, b):\n        self.my_delegate = b\n\n    def foo(self):\n        return "C foo"\n\nc = C(B())\nassert c.foo() == "C foo"\nassert c.bar() == "B bar"\n```\n\n### Validation\n```python\nclass A(metaclass=ABCMeta):\n    @abstractmethod\n    def bar(self):\n        pass\n\n    @abstractmethod\n    def foo(self):\n        pass\n\nclass B:\n    pass\n\n# validation is on by default\nclass C(A, metaclass=delegation_metaclass("_delegate")):\n    def __init__(self, b):\n        self._delegate = b\n\n    def foo(self):\n        return "C foo"\n\nC(B())\n# Trying to instantiate C class with B delegate which is missing \'bar\' method\n# Validation raises an error:\n# TypeError: Can\'t instantiate bar: missing attribute bar in the delegate attribute _delegate\n```\n\n\n### Multiple delegates:\n```python\nfrom abc import ABCMeta\n\nfrom abc_delegation import multi_delegation_metaclass\n\n\nclass A(metaclass=ABCMeta):\n    @abstractmethod\n    def bar(self):\n        pass\n\n    @abstractmethod\n    def foo(self):\n        pass\n\n    @abstractmethod\n    def baz(self):\n        pass\n\nclass B:\n    def bar(self):\n        return "B bar"\n\n    def foo(self):\n        return "B foo"\n\nclass X:\n    def baz(self):\n        return "X baz"\n\nclass C(A, metaclass=multi_delegation_metaclass("_delegate1", "_delegate2")):\n    def __init__(self, d1, d2):\n        self._delegate1 = d1\n        self._delegate2 = d2\n\n    def foo(self):\n        return "C foo"\n\nc = C(B(), X())\nassert c.bar() == "B bar"\nassert c.foo() == "C foo"\nassert c.baz() == "X baz"\n```\n\nPlease refer to the unit tests for more examples.\n',
    'author': 'Vladyslav Halchenko',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monomonedula/abc-delegation',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
