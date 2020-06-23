# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pynetdicom2']

package_data = \
{'': ['*']}

install_requires = \
['pydicom<empty>', 'six']

setup_kwargs = {
    'name': 'pynetdicom2',
    'version': '0.9.1',
    'description': 'pynetdicom2 is a pure python package implementing the DICOM network protocol',
    'long_description': "pynetdicom2\n===========\n\n|docs|\n\npynetdicom2 is a pure python package implementing the DICOM network protocol.\nThis library is a fork/rewrite of the original pynetdicom that can be found here\nhttp://pynetdicom.googlecode.com. Library is not backwards compatible with\noriginal pynetdicom.\n\nLibrary is build on top of pydicom, which is used for reading/writing DICOM\ndatasets. Pynetdicom2 provides implementation for commonly used DICOM services\nsuch as Storage, Query/Retrieve, Verification, etc.\n\nDICOM is a standard (http://medical.nema.org) for communicating medical images\nand related information such as reports and radiotherapy objects.\n\nRoadmap\n=======\n\n* Documentation should really be improved (proper tutorial, some examples)\n* Better test suit (some necessary unit tests and integration tests are\n  missing)\n* Stability and performance improvements. In its current state library performs\n  'good enough', but certainly there is still room for improvement.\n\n.. |docs| image:: https://readthedocs.org/projects/pynetdicom2/badge/?version=latest\n    :alt: Documentation Status\n    :scale: 100%\n    :target: http://pynetdicom2.readthedocs.org/en/latest/",
    'author': "Pavel 'Blane' Tuchin",
    'author_email': 'blane.public@gmail.com',
    'url': 'https://github.com/blanebf/pynetdicom2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
