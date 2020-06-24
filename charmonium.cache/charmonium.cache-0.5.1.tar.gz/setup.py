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
    'version': '0.5.1',
    'description': 'Provides a decorator for caching a function and an equivalent command-line util.',
    'long_description': '================\ncharmonium.cache\n================\n\nProvides a decorator for caching a function and an equivalent\ncommand-line util.\n\nIt wraps an ordinary function. Whenever the function is called with\nthe same arguments, the result is loaded from the cache instead of\ncomputed.\n\nQuickstart\n----------\n\n::\n\n    $ pip install charmonium.cache\n\n.. code:: python\n\n    >>> import charmonium.cache as ch_cache\n    >>> @ch_cache.decor(ch_cache.MemoryStore.create())\n    ... def square(x):\n    ...     print(\'computing\')\n    ...     return x**2\n    ...\n    >>> square(4)\n    computing\n    16\n    >>> square(4) # square is not called again; answer is just looked up\n    16\n    >>> with square.disabled():\n    ...     # disable caching; always recomptue\n    ...     square(4)\n    ...\n    computing\n    16\n\nCustomization\n-------------\n\n``cache_decor`` is flexible because it supports multiple backends.\n\n1. ``MemoryStore``: backed in RAM for the duration of the program (see\n   example above).\n\n2. ``FileStore``: backed in a file which is loaded on first call.\n\n.. code:: python\n\n    >>> import charmonium.cache as ch_cache\n    >>> @ch_cache.decor(ch_cache.FileStore.create("tmp/1"))\n    ... def square(x):\n    ...     return x**2\n    ...\n    >>> # Now that we cache in a file, this is persistent between runs\n    >>> # So I must clear it here.\n    >>> square.clear()\n    >>> list(map(square, range(5)))\n    [0, 1, 4, 9, 16]\n    >>> import os\n    >>> os.listdir("tmp/1")\n    [\'__main__.square_cache.pickle\']\n\n3. ``DirectoryStore``: backed in a directory. Results are stored as\n   individual files in that directory, and they are loaded lazily. Use\n   this for functions that return large objects.\n\n.. code:: python\n\n    >>> import charmonium.cache as ch_cache\n    >>> @ch_cache.decor(ch_cache.DirectoryStore.create("tmp/2"))\n    ... def square(x):\n    ...     return x**2\n    ...\n    >>> # Now that we cache in a file, this is persistent between runs\n    >>> # So I must clear it here.\n    >>> square.clear()\n    >>> list(map(square, range(5)))\n    [0, 1, 4, 9, 16]\n    >>> import os\n    >>> sorted(os.listdir("tmp/2/__main__.square"))\n    [\'(0).pickle\', \'(1).pickle\', \'(2).pickle\', \'(3).pickle\', \'(4).pickle\']\n\n4. Custom stores: to create a custom store, just extend ``ObjectStore``\n   and implement a dict-like interface.\n\n``FileStore`` and ``DirectoryStore`` can both themselves be customized by:\n\n- Providing a ``cache_path`` (conforming to the ``PathLike`` interface),\n  e.g. one can transparently cache in AWS S3 with an `S3Path`_ object.\n\n.. _`S3Path`: https://pypi.org/project/s3path/\n\n- Providing a ``serializer`` (conforming to the ``Serializer`` interface),\n  e.g. `pickle`_ (default), `cloudpickle`_, `dill`_, or `messagepack`_.\n\n.. _`pickle`: https://docs.python.org/3/library/pickle.html\n.. _`cloudpickle`: https://github.com/cloudpipe/cloudpickle\n.. _`dill`: https://github.com/uqfoundation/dill\n.. _`messagepack`: https://github.com/msgpack/msgpack-python\n\n``cache_decor`` also takes a "state function" which computes the value\nof some external state that this computation should depend on. Unlike\nthe arguments (which the cache explicitly depends on), values computed\nwith a different state are evicted out, so this is appropriate when\nyou never expect to revisit a prior state (e.g. modtime of a file\ncould be a state, as in ``make_file_state_fn``).\n\nWith ``verbose=True``, this will output to a logger.\n\n.. code:: python\n\n    >>> import charmonium.cache as ch_cache\n    >>> @ch_cache.decor(ch_cache.MemoryStore.create(), verbose=True)\n    ... def square(x):\n    ...     print(\'computing\')\n    ...     return x**2\n    ...\n    >>> square(4) # doctest:+SKIP\n    2020-06-19 11:31:40,197 - __main__.square: miss with args: (4,), {}\n    computing\n    16\n    >>> square(4) # doctest:+SKIP\n    2020-06-19 11:31:40,197 - __main__.square: hit with args: (4,), {}\n    16\n\nCLI\n---\n\n::\n\n    # cache a commandline function based on its args\n    $ cache --verbose -- compute_square 6\n    miss for square(["6"])\n    36\n\n    $ cache -- compute_square 6\n    hit for square(["6"])\n    36\n',
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
