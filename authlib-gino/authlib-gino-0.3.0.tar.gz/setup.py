# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['authlib_gino',
 'authlib_gino.async_grants',
 'authlib_gino.fastapi_session',
 'authlib_gino.fastapi_session.migrations',
 'authlib_gino.fastapi_session.migrations.versions',
 'authlib_gino.gino_oauth2',
 'authlib_gino.starlette_oauth2']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=0.14.3,<0.15.0', 'gino>=1.0.1,<2.0.0']

extras_require = \
{'app': ['fastapi>=0.55.1,<0.56.0',
         'alembic>=1.4.2,<2.0.0',
         'psycopg2-binary>=2.8.5,<3.0.0',
         'python-multipart>=0.0.5,<0.0.6'],
 'starlette': ['starlette>=0.13.2,<0.14.0']}

entry_points = \
{'gino.app.extensions': ['session.admin = '
                         'authlib_gino.fastapi_session.admin:init_app',
                         'session.demo = '
                         'authlib_gino.fastapi_session.demo_login:init_app',
                         'session.oidc = '
                         'authlib_gino.fastapi_session.oidc:init_app'],
 'gino.app.migrations': ['session.oidc = '
                         'authlib_gino.fastapi_session:migrations']}

setup_kwargs = {
    'name': 'authlib-gino',
    'version': '0.3.0',
    'description': 'OpenID Connect provider implemented with Authlib and GINO.',
    'long_description': None,
    'author': 'Fantix King',
    'author_email': 'fantix.king@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
