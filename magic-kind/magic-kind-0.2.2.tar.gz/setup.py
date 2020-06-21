# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_kind']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'magic-kind',
    'version': '0.2.2',
    'description': 'The MagicKind type is a simpler alternative to Enum types for groups of related magic values when order is not important.',
    'long_description': '# magic-kind\n\nThe MagicKind type is a simpler alternative to Enum types for groups of\nrelated magic values when order is not important.\n\n### Synopsis:\n\n```\nfrom magic_kind import MagicKind\n\nclass HttpCode(MagicKind):\n    OK = 200\n    NOT_FOUND = 404\n    GATEWAY = 503\n  \n...\n\nraise HttpException(HttpCode.NOT_FOUND, ...)\n    \n...\n\nassert http_code in HttpCode\n\n...\n\nfor http_code in HttpCode:\n    print(http_code)\n````\n\n### Motivation\n\nThink of the kind of things you might put in a constants.py file to make\nsure you use the value consistently across your application. And then think\nabout the times such magic values were really just one of a number of\nalternatives. For example they were all different Http Code values like:\n\n```\nHTTP_CODE_OK = 200\nHTTP_CODE_NOT_FOUND = 404\nHTTP_CODE_GATEWAY = 503\n```\n\nThis is the kind of case that the the MagicKind type is made for. Instead\none would do this:\n\n```\nclass HttpCode(MagicKind):\n    OK = 200\n    NOT_FOUND = 404\n    GATEWAY = 503\n```\n\nThe class itself provides some container object like functionality. It\nallows you to iterate over it and get the values, and it allows you to use the\n***in*** operator to check if a value you got somewhere else is in the Choices.\n\n### But why not just use Enum instead?\nEnumerated types have a similar but broader functionality where they are like\ncontainers with special objects that know their relative order and have\nattributes for their "name" and "value".\n\nMagicKind types are instead like containers of the values themselves. This\nmakes dealing with them easier unless there is some special reason you are\ninterested in the order and attribute names as well as the values.\n\nTo illustrate the difference, let us suppose some user entered data is stored\nas **some_string** and we wish to know if it is one of our kinds of soda:\n\n```python\nclass Soda(str, Enum):\n    ROOT_BEER = "root beer"\n    COLA = "cola"\n    \nvalid_soda_values = set([_.value for _ in Soda])\n\nif some_string in valid_soda_values:\n    print(f"{some_string} is a soda")\n```\nWith MagicKind the basic elements are just the values "root beer" and "cola",\nso we don\'t need to make a **valid_soda_values** set:\n\n```python\nclass Soda(MagicKind):\n    ROOT_BEER = "root beer"\n    COLA = "cola"\n    \nif some_string in Soda:\n    print(f"{some_string} is a soda")\n```\n\n### Usage Rules:\n1. To be recognized as one of the choices, attribute names must be\n       upper case identifiers that do not begin with an underscore. This\n       is by design to allow other kinds of members to be added (methods\n       for example, or other attributes that are not meant to be choices).\n2. The values must be hashable (they are stored in a set internally). It\n       is recommended that they are also immutable.\n3. The upper case choice values should never be changed nor should they \nbe replaced. Doing so will cause the internal metaclass data to be wrong and\n trouble will likely follow. If you want some non-constant class values, don\'t\n make them upper case, and they won\'t be seen as one of the magic value choices.\n4. The following pre-existing non-choice members should not be overwritten:\n\n| name | what it is already used for |\n| --- | --- |\n| **get_dict** | method that gets dict of magic value attribute names and values |\n| **get_names** | method that gets set of magic value attribute names |\n| **_choices_dict** | internal use by MetaMagicKind metaclass |\n| **_choices_set** | internal use by MetaMagicKind metaclass |\n| **_pydantic_validate** | along with **\\_\\_get_validators\\_\\_** provided to support use of MagicKind [in pydantic models](https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types) |\n\nIn addition, all \\_\\_special\\_\\_ variable names should only be overloaded if you know what you are doing.\n\n### Works with Pydantic \nFor those who wish to declare the MagicKind type in a\n[pydantic model](https://pydantic-docs.helpmanual.io/usage/models/), MagicKind\nhas a validator method that behaves just as one expects (it will only accept\none of the "magic values" for the subclass).\n\n### Acknowledgement\nThis package was originally developed at Rackspace Technology, which is releasing it\nto the public under the Apache 2 open source license.\n',
    'author': 'andr3738',
    'author_email': 'andr3738@rackspace.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aallaire/magic-kind',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
