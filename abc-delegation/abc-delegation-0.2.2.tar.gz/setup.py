# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abc_delegation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'abc-delegation',
    'version': '0.2.2',
    'description': 'A tool for automated delegation with abstract base classes',
    'long_description': '# abc-delegation\n\nA tool for automated delegation with abstract base classes.\n\nThis metaclass enables creation of delegating classes \ninheriting from an abstract base class. \n\nThis technique is impossible with regular `__getattr__` approach for delegation,\nso normally, you would have to define every delegated method explicitly.\nNot any more\n\nInstallation:\n`pip install abc-delegation`\n\n\nBasic usage:\n```python    \nfrom abc import ABCMeta\n\nfrom abc_delegation import delegation_metaclass\n\nclass A(metaclass=ABCMeta):\n    @abstractmethod\n    def bar(self):\n        pass\n\n    @abstractmethod\n    def foo(self):\n        pass\n\nclass B:\n    def bar(self):\n        return "B bar"\n\n    def foo(self):\n        return "B foo"\n\nclass C(A, metaclass=delegation_metaclass("my_delegate")):\n    def __init__(self, b):\n        self.my_delegate = b\n\n    def foo(self):\n        return "C foo"\n\nc = C(B())\nassert c.foo() == "C foo"\nassert c.bar() == "B bar"\n```\n\nMultiple delegates:\n```python\nfrom abc import ABCMeta\n\nfrom abc_delegation import multi_delegation_metaclass\n\n\nclass A(metaclass=ABCMeta):\n    @abstractmethod\n    def bar(self):\n        pass\n\n    @abstractmethod\n    def foo(self):\n        pass\n\n    @abstractmethod\n    def baz(self):\n        pass\n\nclass B:\n    def bar(self):\n        return "B bar"\n\n    def foo(self):\n        return "B foo"\n\nclass X:\n    def baz(self):\n        return "X baz"\n\nclass C(A, metaclass=multi_delegation_metaclass("_delegate1", "_delegate2")):\n    def __init__(self, d1, d2):\n        self._delegate1 = d1\n        self._delegate2 = d2\n\n    def foo(self):\n        return "C foo"\n\nc = C(B(), X())\nassert c.bar() == "B bar"\nassert c.foo() == "C foo"\nassert c.baz() == "X baz"\n```\n',
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
