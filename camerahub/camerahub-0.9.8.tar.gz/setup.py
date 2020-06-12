# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camerahub',
 'help',
 'help.migrations',
 'schema',
 'schema.migrations',
 'schema.templatetags']

package_data = \
{'': ['*'],
 'help': ['templates/*'],
 'schema': ['static/*',
            'static/css/*',
            'static/logos/*',
            'static/svg/*',
            'templates/*',
            'templates/schema/*',
            'templates/watson/includes/*']}

install_requires = \
['Django>=2.2.13,<3.0.0',
 'awesome-slugify>=1.6.5,<2.0.0',
 'django-autosequence>=0,<1',
 'django-choices>=1.7.0,<2.0.0',
 'django-crispy-forms>=1.9.0,<2.0.0',
 'django-currentuser>=0.5,<0.6',
 'django-favicon>=0.1.3,<0.2.0',
 'django-filter>=2.2,<3.0',
 'django-fullurl>=1,<2',
 'django-getenv>=1.3.2,<2.0.0',
 'django-money>=0.15,<0.16',
 'django-prometheus>=2.0.0,<3.0.0',
 'django-redis>=4.11,<5.0',
 'django-registration>=3.0,<4.0',
 'django-sendgrid-v5>=0,<1',
 'django-tables2>=2.1.1,<3.0.0',
 'django-taggit>=1,<2',
 'django-watson>=1.5.5,<2.0.0',
 'poetry-version',
 'pytz',
 'uWSGI>=2.0.0,<3.0.0']

extras_require = \
{'pgsql': ['psycopg2-binary>=2.8,<3.0']}

setup_kwargs = {
    'name': 'camerahub',
    'version': '0.9.8',
    'description': 'App for cataloguing vintage cameras, lenses, films, negatives & prints',
    'long_description': '# CameraHub\n\nCameraHub is a web app for film photography that can be used to track cameras, lenses, accessories, films, negatives and prints, to fully\ncatalogue a collection of photographic equipment as well as the pictures that are made with them.\n\nIt replaces an earlier command-line project, called [PhotoDB](https://github.com/djjudas21/photodb-perl), which has now been deprecated.\n\n## Installing CameraHub\n\nThere are several ways of installing CameraHub, depending on your needs:\n\n* With Pip\n* [From source](docs/INSTALL_SOURCE.md)\n* [With Docker](docs/INSTALL-DOCKER.md)\n* [With Kubernetes](docs/INSTALL-KUBERNETES.md)\n\n## Configuring CameraHub\n\nCameraHub requires almost no additional config to run with default settings. However it is insecure in this configuration so at least `CAMERAHUB_SECRET_KEY` and\n`CAMERAHUB_PROD` must be set if you are running in production.\n\nThe following environment variables are supported:\n\n| Variable                   | Use                                                                                              | Default                      |\n|----------------------------|--------------------------------------------------------------------------------------------------|------------------------------|\n| `CAMERAHUB_ADMIN_EMAIL`    | email address for the `admin` account                                                            | `admin@example.com`          |\n| `CAMERAHUB_ADMIN_PASSWORD` | password for the `admin` account                                                                 | `admin`                      |\n| `CAMERAHUB_DB_ENGINE`      | [database engine](https://docs.djangoproject.com/en/3.0/ref/settings/#engine)                    | `django.db.backends.sqlite3` |\n| `CAMERAHUB_DB_HOST`        | [database hostname or IP address](https://docs.djangoproject.com/en/3.0/ref/settings/#host)      |                              |\n| `CAMERAHUB_DB_NAME`        | [database schema or path to SQLite db](https://docs.djangoproject.com/en/3.0/ref/settings/#name) | `db/db.sqlite3`              |\n| `CAMERAHUB_DB_PASS`        | [database password](https://docs.djangoproject.com/en/3.0/ref/settings/#password)                |                              |\n| `CAMERAHUB_DB_PORT`        | [database port](https://docs.djangoproject.com/en/3.0/ref/settings/#port)                        |                              |\n| `CAMERAHUB_DB_USER`        | [database username](https://docs.djangoproject.com/en/3.0/ref/settings/#user)                    |                              |\n| `CAMERAHUB_PROD`           | enable [Django production mode](https://docs.djangoproject.com/en/3.0/ref/settings/#debug)       | `false`                      |\n| `CAMERAHUB_SECRET_KEY`     | random secret value. Generate [here](https://miniwebtool.com/django-secret-key-generator/)       | `OverrideMe!`                |\n| `CAMERAHUB_SENDGRID_KEY`   | API key for Sendgrid email backend                                                               |                              |\n| `CAMERAHUB_FROM_EMAIL`     | [from email address](https://docs.djangoproject.com/en/3.0/ref/settings/#default-from-email)     | `noreply@camerahub.info`     |\n| `CAMERAHUB_DOMAIN`         | [site domain](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts)                 | `camerahub.info`             |\n| `CAMERAHUB_REDIS`          | enable [Redis caching](https://docs.djangoproject.com/en/3.0/topics/cache/)                      | `false`                      |\n| `CAMERAHUB_REDIS_HOST`     | Redis hostname or IP address                                                                     | `127.0.0.1`                  |\n| `CAMERAHUB_REDIS_PORT`     | Redis port                                                                                       | `6379`                       |\n\n## See also\n\n* [Screenshots](docs/SCREENSHOTS.md)\n* [Contributing](docs/CONTRIBUTING.md)\n* [Changelog](https://github.com/djjudas21/camerahub/releases)\n* [Icons](docs/ICONS.md)\n',
    'author': 'Jonathan Gazeley',
    'author_email': 'camerahub@jonathangazeley.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://camerahub.info/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
