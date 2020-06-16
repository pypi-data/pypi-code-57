# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serdataclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'serdataclasses',
    'version': '0.7.0',
    'description': 'Serialize/deserialize Python objects from/to typed structures.',
    'long_description': '# serdataclasses\n\n[![image-version](https://img.shields.io/pypi/v/serdataclasses.svg)](https://python.org/pypi/serdataclasses)\n[![image-license](https://img.shields.io/pypi/l/serdataclasses.svg)](https://python.org/pypi/serdataclasses)\n[![image](https://img.shields.io/pypi/pyversions/serdataclasses.svg)](https://python.org/pypi/serdataclasses)\n[![image-ci](https://github.com/pappasam/serdataclasses/workflows/serdataclasses%20ci/badge.svg)](https://github.com/pappasam/serdataclasses/actions?query=workflow%3A%22serdataclasses+ci%22)\n\nThis library has the following goals:\n\n1. "Deserialize" unstructured Python types into structured, type-hinted Python types (dataclasses.dataclass, typing.NamedTuples).\n2. "Serialize" structured, type-hinted Python objects into unstructured Python types (eg, the reverse)\n3. Provide the user clear error messages in the event that serde fails.\n4. Require no type changes on the part of the user. No need to give your containers a special type to help this library perform serde, it works out of the box.\n5. [Optionally] automatically convert primitive types, but stop converting when ambiguous types are encountered (`Union`), but handle the special case of `Optional`, which is used in many codebases.\n6. Work correctly for all forms of NamedTuples and dataclasses. Unfortunately, prior to Python 3.8, the dataclasses had some deficiencies. Mainly, `dataclasses.InitVar` was a singleton whose contained type could not be inspected at runtime. For this reason, only Python 3.8+ is supported.\n\nNo external dependencies. Python 3.8+.\n\n## Installation\n\n```bash\n# With pip\npip install serdataclasses\n\n# With poetry\npoetry add serdataclasses\n```\n\n## Usage\n\n```python\nimport dataclasses\nimport typing\nimport serdataclasses\n\n@dataclasses.dataclass\nclass SmallContainer:\n    my_str: str\n\n@dataclasses.dataclass\nclass BigContainer:\n    my_int: int\n    my_list: typing.List[SmallContainer]\n\nMY_DATA = {\n    "my_int": 1,\n    "my_list": [\n        { "my_str": "rawr" },\n        { "my_str": "woof" },\n    ],\n}\n\n# Deserialization\nMY_STRUCTURED_DATA = serdataclasses.load(MY_DATA, BigContainer)\nprint("Deserialization:", MY_STRUCTURED_DATA)\n\n# Serialization\nMY_UNSTRUCTURED_DATA_AGAIN = serdataclasses.dump(MY_STRUCTURED_DATA)\nprint("Serialization:", MY_UNSTRUCTURED_DATA_AGAIN)\n```\n\nResult:\n\n```console\nDeserialization: BigContainer(my_int=1, my_list=[SmallContainer(my_str=\'rawr\'), SmallContainer(my_str=\'woof\')])\nSerialization: {\'my_int\': 1, \'my_list\': [{\'my_str\': \'rawr\'}, {\'my_str\': \'woof\'}]}\n```\n\n## Local Development\n\nLocal development for this project is quite simple.\n\n**Dependencies**\n\nInstall the following tools manually.\n\n* [Poetry](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n*Recommended*\n\n* [asdf](https://github.com/asdf-vm/asdf)\n\n**Set up development environment**\n\n```bash\nmake setup\n```\n\n**Run Tests**\n\n```bash\nmake test\n```\n\n## Notes\n\n* Initially inspired by [undictify](https://github.com/Dobiasd/undictify) and a PR I helped with. serdataclasses\'s goals are different; it\'s exclusively focused on serde instead of general function signature overrides.\n* I also notice some striking similarities with a library called [typedload](https://github.com/ltworf/typedload) (great minds think alike, I guess :p). I renamed my top-level functions to "load" and "dump" in typedload\'s homage. Unfortunately, as of version `1.20`, typedload does not handle all types of dataclasses elegantly (mainly, InitVar). Since typedload supports Python 3.5+, it never will elegantly handle all dataclasses without lots of unfortunate conditionals in the codebase. If you must use Python 3.7-, I suggest looking into typedload.\n\n## Written by\n\nSamuel Roeca *samuel.roeca@gmail.com*\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pappasam/serdataclasses',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
