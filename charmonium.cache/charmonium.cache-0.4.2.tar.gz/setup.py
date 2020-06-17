# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['charmonium', 'charmonium.cache']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cache = charmonium.cache._cli:main']}

setup_kwargs = {
    'name': 'charmonium.cache',
    'version': '0.4.2',
    'description': 'Provides a decorator for caching a function and an equivalent command-line util.',
    'long_description': '================\ncharmonium.cache\n================\n\nProvides a decorator for caching a function and an equivalent\ncommand-line util.\n\nIt wraps an ordinary function. Whenever the function is called with\nthe same arguments, the result is loaded from the cache instead of\ncomputed.\n\nQuickstart\n----------\n\n::\n\n    $ pip install charmonium.cache\n\n::\n\n    >>> import charmonium.cache as ch_cache\n    >>> @ch_cache.decor(ch_cache.MemoryStore.create())\n    ... def square(x):\n    ...     print(\'computing\')\n    ...     return x**2\n    ...\n    >>> square(4)\n    computing\n    16\n    >>> square(4) # square is not called again; answer is just looked up\n    16\n\nCustomization\n-------------\n\n`cache_decor` is flexible because it supports multiple backends.\n\n1. `MemoryStore`: backed in RAM for the duration of the program\n\n2. `FileStore`: backed in an index file which is loaded on first call.\n\n3. `DirectoryStore`: backed in a directory. Results are stored as\n   individual files in that directory, and they are loaded lazily. Use\n   this for functions that return large objects.\n\n4. Custom stores: to create a custom store, just extend `ObjectStore`\n   and implement a dict-like interface.\n\n`FileStore` and `DirectoryStore` can both themselves be customized by:\n\n- Providing a `cache_path`  (conforming to the `PathLike` interface), e.g. an `S3Path` object.\n\n- Providing a `serializer` (conforming to the `Serializer` interface), e.g. [pickle] (default), [cloudpickle], [dill], [messagepack].\n\n`cache_decor` also takes a "state function" which computes the value\nof some external state that this computation should depend on. Unlike\nthe arguments (which the cache explicitly depends on), values computed\nwith a different state are evicted out, so this is appropriate when\nyou never expect to revisit a prior state (e.g. modtime of a file\ncould be a state, as in `make_file_state_fn`).\n\nCLI\n---\n\n::\n\n    # cache a commandline function based on its args\n    read n\n    cache -- compute_prime ${n}\n\n    # cache based on args AND file-modtime\n    # recompiles when main.c is newer than the most recent compile\n    cache --file main.c -- gcc main.c -o main\n',
    'author': 'Samuel Grayson',
    'author_email': 'sam+dev@samgrayson.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/charmoniumQ/charmonium.cache.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
