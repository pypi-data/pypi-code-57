# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_x_bugsnag']

package_data = \
{'': ['*']}

install_requires = \
['bugsnag>=3.6.0,<4.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'starlette>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'starlette-x-bugsnag',
    'version': '0.1.5',
    'description': 'Shiny Bugsnag integration for Starlette framework',
    'long_description': '# starlette-x-bugsnag\n\nShiny [Bugsnag](https://www.bugsnag.com/) integration for [Starlette](https://www.starlette.io/) framework ✨\n\n![test](https://github.com/2tunnels/starlette-x-bugsnag/workflows/test/badge.svg?branch=master)\n![codecov](https://img.shields.io/codecov/c/github/2tunnels/starlette-x-bugsnag/master)\n![dependencies](https://img.shields.io/librariesio/release/pypi/starlette-x-bugsnag)\n![version](https://img.shields.io/pypi/v/starlette-x-bugsnag.svg)\n![pyversions](https://img.shields.io/pypi/pyversions/starlette-x-bugsnag.svg)\n![black](https://img.shields.io/badge/code%20style-black-000000.svg)\n![license](https://img.shields.io/pypi/l/starlette-x-bugsnag)\n\n[Scope](https://asgi.readthedocs.io/en/latest/specs/main.html#connection-scope) details,\nlocal variables and installed packages will be attached to each event for ease of debugging.\n\nInstallation:\n\n```sh\npip install starlette-x-bugsnag\n```\n\nUsage:\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette.middleware import Middleware\nfrom starlette.requests import Request\nfrom starlette.responses import JSONResponse\nfrom starlette.routing import Route\n\nfrom starlette_x_bugsnag.middleware import BugsnagMiddleware\n\n\nasync def home(request: Request) -> JSONResponse:\n    return JSONResponse({"message": "Hello world!"})\n\n\nroutes = [Route("/", home)]\n\n# Using application constructor\napplication = Starlette(\n    routes=routes, middleware=[Middleware(BugsnagMiddleware, api_key="secret")],\n)\n\n# Or using add_middleware method\napplication.add_middleware(BugsnagMiddleware, api_key="secret")\n```\n\n`BugsnagMiddleware` accepts same arguments as `bugsnag.configure` function, so you can pass additional information\nabout your app, such as `app_version`.\n\n```python\napplication = Starlette(\n    routes=routes,\n    middleware=[\n        Middleware(\n            BugsnagMiddleware,\n            api_key="secret",\n            app_version="1.2.3",\n            release_stage="production",\n            project_root=None,  # Save traceback not only from the current directory\n        ),\n    ],\n)\n```\n',
    'author': 'Vlad Dmitrievich',
    'author_email': 'me@2tunnels.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2tunnels/starlette-x-bugsnag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
