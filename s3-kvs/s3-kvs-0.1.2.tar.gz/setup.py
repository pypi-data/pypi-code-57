# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['s3_kvs']
install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 's3-kvs',
    'version': '0.1.2',
    'description': 'Python wrapper for an AWS S3 backed key-value store.',
    'long_description': 's3-kvs\n======\n\nA python wrapper for an S3 backed key-value store.\n\nUsage\n=====\n\nImport and create a client instance, setting a domain and optionally a namespace:\n\n\n    from s3_kvs import ReadOnlyClient\n\n    client = ReadOnlyClient(domain=\'kvs.example.com\')\n\n    OR\n\n    client = ReadOnlyClient(domain=\'kvs.example.com\', namespace=\'test\')\n\n\nThen use then use the getitem notation to retrieve values from the key store:\n\n    client[\'foo\']\n\n    > \'bar\'\n\nOr, use the get method to provide a default if no matching value is found:\n\n    client.get(\'foo\', \'oops\')\n\n    > \'oops\'\n\nBy default returned values are text. You can also treat them as json and automatically parse them:\n\n    text_client = ReadOnlyClient(domain=\'kvs.example.com\')\n\n    client[\'foo\']\n\n    > \'{"bar": "baz"}\'  # a json string\n\n    json_client = ReadOnlyClient(domain=\'kvs.example.com\', value_format=\'json\')\n\n    client[\'foo\']\n\n    > {\'bar\': \'baz\'}  # a python dict\n',
    'author': 'Richard Campen',
    'author_email': 'richard@campen.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octavenz/s3-kvs',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
