# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockontext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dockontext',
    'version': '0.1.3',
    'description': 'context manager that runs and closes docker containers',
    'long_description': '# dockontext\n[![pypi](https://img.shields.io/pypi/v/dockontext.svg)](https://pypi.python.org/pypi/dockontext)\n[![Build Status](https://travis-ci.com/ghsang/dockontext.svg?branch=master)](https://travis-ci.com/ghsang/dockontext)\n[![codecov](https://codecov.io/gh/ghsang/dockontext/branch/master/graph/badge.svg)](https://codecov.io/gh/ghsang/dockontext)\n\n\n### context manager that runs and closes docker containers\n* When integration or end-to-end test needs temporal docker container to fake remote systems, this package will help to create/close/remove the temporal docker container.\n\n### Features\n* Create docker container by giving image name. The container will be named as \'docontext={name}\'\n* Close and remove the container when exit.\n\n### Example\n\n#### pytest.fixture\n```\nimport pytest\nfrom dockontext import container_generator_from_image, Result, Config\n\ncreate_container = pytest.fixture(container_generator_from_image)\n\ndef test_fixture(create_container):\n     config = Config(name, "alpine:latest")\n     container = create_container(config)\n     result = container.execute("echo hello", timeout: float)\n     assert result == Result(returncode=0, stdout="hello\\n", stderr="")\n```\n\n\n### TODO\n* Dockerfile\n* docker-compose.yml\n* container group context\n\n### Free software: MIT License\n\n\n### Credits\n\n* This package was created with [Cookiecutter][1]\n* Also was copied and modified from the [audreyr/cookiecutter-pypackage][2] project template.\n\n[1]: https://github.com/cookiecutter/cookiecutter\n[2]: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Hyuksang Gwon',
    'author_email': 'gwonhyuksang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ghsang/dockontext',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
