# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockontext']

package_data = \
{'': ['*']}

install_requires = \
['codecov>=2.1.7,<3.0.0']

setup_kwargs = {
    'name': 'dockontext',
    'version': '0.1.0',
    'description': 'context manager that runs and closes docker containers',
    'long_description': '# dockontext\n[![pypi](https://img.shields.io/pypi/v/dockontext.svg)](https://pypi.python.org/pypi/dockontext)\n[![Build Status](https://travis-ci.com/ghsang/dockontext.svg?branch=master)](https://travis-ci.com/ghsang/dockontext)\n[![codecov](https://codecov.io/gh/ghsang/dockontext/branch/master/graph/badge.svg)](https://codecov.io/gh/ghsang/dockontext)\n\n\n### context manager that runs and closes docker containers\n\n### Features\n* When integration or end-to-end test needs temporal docker container to fake remote systems, this package will help to create/close/remove the temporal docker container.\n\n### Example\n\n#### with pytest.fixture\n```\nimport pytest\nfrom dockontext import container_generator_from_image, Result\n\ndocker_context = pytest.fixture(container_generator_from_image)\n\n@pytest.mark.asyncio\nasync def test_fixture(docker_context):\n     # container will be created and the name is \'dockontext-{name}\'\n     async with docker_context(name, "alpine:latest") as container:\n         result = await container.execute(name, timeout: float)\n         assert result == Result(returncode=0, stdout="hello\\n", stderr="")\n     # container will be stopped and removed here\n```\n\n#### with contextlib.asynccontextmanager\n```\nfrom contextlib import asynccontextmanager\nfrom dockontext import container_generator_from_image, Result\n\ndocker_context = asynccontextmanager(container_generator_from_image)\n```\n\n\n### TODO\n* Dockerfile\n* docker-compose.yml\n* container group context\n* get ip\n\n### Free software: MIT License\n\n\n### Credits\n\n* This package was created with [Cookiecutter][1]\n* Also was copied and modified from the [audreyr/cookiecutter-pypackage][2] project template.\n\n[1]: https://github.com/cookiecutter/cookiecutter\n[2]: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Hyuksang Gwon',
    'author_email': 'gwonhyuksang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ghsang/dockontext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
