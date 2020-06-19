# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duckt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'duckt',
    'version': '0.1.0',
    'description': 'Python package facilitating duck typing through attribute traverse utilities',
    'long_description': '# duck\nA small Python package facilitating duck typing through attribute traverse utilities\n\nThis replaces try/except chains when trying to call different methods:\n```python\nfrom duckt import Duck, DuckCall\n\nclass Lion:\n    def roar(self):\n        return "roar!"\n\ncreature = Lion()\nassert Duck(creature).attr_call(\n    DuckCall("make_sound", ["woof"]), # tries to call creature.make_sound("woof")\n    DuckCall("make_sound", ["buzz", 100]), # tries to call creature.buzz("buzz", 100)\n    DuckCall("bark"), # creature.bark()\n    DuckCall("roar"), # creature.roar()\n    DuckCall("speak", ["Hello "], {"times": 3}) # creature.speak("Hello ", times=3)\n) == "roar!"\n\n # returns the output of the first successfull call\n# if none of the call attempts was successful then the last raised error will be thrown\n```\n**DuckCall** class is fully replacable here with any custom callable accepting single argument. This argument is the **Duck**-wrapped object, so you can implement custom attribute extracting and/or calling behavior here. **AttributeError**s and **TypeError**s thrown from this callable is handled by the **Duck** instance.\n\n\nSimplified interface for property extraction:\n```python\nfrom duckt import Duck\n\nclass Person:\n    full_name = "John Doe"\n\nsome_person = Person()\nname = Duck(some_person).attr(\'first_name\', \'name\', \'full_name\')\n# name now is equal to the first present attribute\n# otherwise AttributeError is thrown\n```\n\nYou may also use **Duck** as wrapper to a callable:\n```python\nfrom duckt import Duck\n\ndef foo(some_string):\n    print(some_string)\n\nduck = Duck(foo)\nduck.call(\n    ["hello", "world"], # foo("hello", "world")\n    ["hello world"],    # foo("hello world")\n    [[], {"hello": "world"}]  # foo(hello="world")\n)\n\n```\nThat\'s it.\n',
    'author': 'Vladyslav Halchenko',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monomonedula/duck',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
