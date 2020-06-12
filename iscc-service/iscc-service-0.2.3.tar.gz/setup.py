# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_service']

package_data = \
{'': ['*']}

install_requires = \
['bitstring>=3.1,<4.0',
 'fastapi>=0.54,<0.55',
 'iscc-cli>=0.9,<0.10',
 'jmespath>=0.9,<0.10',
 'loguru>=0.4,<0.5',
 'mcrpc>=2.0,<3.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.11,<0.12']

entry_points = \
{'console_scripts': ['isccservice = iscc_service.main:run_server']}

setup_kwargs = {
    'name': 'iscc-service',
    'version': '0.2.3',
    'description': 'ISCC Web Service API',
    'long_description': "# iscc-service - ISCC Web Service API\n[![Version](https://img.shields.io/pypi/v/iscc-service.svg)](https://pypi.python.org/pypi/iscc-service/)\n[![Downloads](https://pepy.tech/badge/iscc-service)](https://pepy.tech/project/iscc-service)\n[![Pulls](https://shields.beevelop.com/docker/pulls/titusz/iscc-service.svg?style=flat-square)](https://hub.docker.com/r/titusz/iscc-service)\n\n> A REST OpenAPI Backend for creating [**ISCC codes**](https://iscc.codes) for digital media files.\n\n\n**Note**: This is work in progress. Use with care and at your own risk\n\nThe Webservice is build with [FastAPI](https://github.com/tiangolo/fastapi) and makes\nuse of the [ISCC reference implementation](<https://github.com/iscc/iscc-specs>) and\nthe [ISCC Command Line Tool](https://github.com/iscc/iscc-cli) and includes an\ninteractive API documentation:\n\n![Interactive ISCC Api Docs](screenshot.jpg)\n\n\nThe Docker image is published at https://hub.docker.com/r/titusz/iscc-service\n\n\n## Setup for development\n\nIf you are using [poetry](https://python-poetry.org/):\n\n- After checkout cd into code directory and run 'poetry install' to install dependencies.\n- Launch dev server with: 'uvicorn iscc_service.main:app --reload'\n- See API docs at: http://127.0.0.1:8000\n\nFor the 'lookup' endpoint to work you must provide env variables for node connection.\nSee [config.py](iscc_service/config.py)\n\n## Install via pip\n\n```bash\n$ pip3 install iscc-service\n```\n\nRun webservice via uvicorn\n\n```bash\n$ isccservice\nINFO:     Started server process [18800]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\n```\n\n## Publishing on Docker HUB:\n\n```bash\ndocker login\ndocker build -t iscc-service -f Dockerfile .\ndocker run --rm -p 8080:8080 -it iscc-service\ndocker tag iscc-service username/iscc-service:0.1.9\ndocker push username/iscc-service:0.1.9\n```\n\n## Change Log\n\n### [0.2.3] - 2020-06-12\n- Use vendorized tika\n\n### [0.2.2] - 2020-06-12\n- Update to iscc-cli 0.9.11\n\n### [0.2.1] - 2020-05-13\n- Update to iscc-cli 0.9.8\n- More conservative lookup matching\n\n### [0.2.0] - 2020-05-01\n- Update to support flac and opus audio files\n\n### [0.1.9] - 2020-04-27\n\n- Support updated Content-ID Audio\n- Support incomplete ISCC codes\n- Updated dependencies\n\n### [0.1.8] - 2020-03-02\n\n- Add support for mobi files\n- Initial pypi release\n\n\n## License\n\nMIT © 2019-2020 Titusz Pan\n",
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iscc.codes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
