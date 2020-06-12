# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['happy_quotas', 'happy_quotas.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dj-happy-quotas',
    'version': '0.1.0',
    'description': 'Transaction-based quotas for Django',
    'long_description': "# dj-happy-quotas\n\nTransaction-based quotas for Django.\n\n## Introduction\n\nBelieve it or not, but some users really don't enjoy signing up for monthly or annual subscription plans. And for some applications such subscriptions also don't really make much sense, like when they are best used ocassionally by means of single-fire transactions.\n\nThis package provides handling of transaction-like quotas that a user can fill up on demand.\n\nHandling of pricing plans and payments are not subject of this package.\n\n## Use\n\nInstall:\n\n```console\npoetry add dj-happy-quotas\n```\n\n(A mere `pip install dj-happy-quotas` might work as well.)\n\nAdd to `INSTALLED_APPS` in `settings.py`:\n\n```python\nINSTALLED_APPS = [\n    ...\n    'dj-happy-quotas',\n    ...\n]\n```\n\nRun database migrations:\n\n```\npython manage.py migrate dj-happy-quotas\n```\n\n## Publishing a new release\n\n```sh\n# Update version number in pyproject.toml and happy_quotas/__init__.py\n\n# Check that everything looks ok\npoetry config --list\npoetry check\n\n# Publish\npoetry build\npoetry publish\n```\n\n## Related projects\n\n* [django-billing](https://github.com/gabrielgrant/django-billing) for a very similar approach to this one here but being more generic in targetting recurring billing on top.\n* [django-flexible-subscriptions](https://github.com/studybuffalo/django-flexible-subscriptions) for handling of subscriptions where authentication is plugged via Django's standard groups.\n* [django-plans](https://github.com/django-getpaid/django-plans) for subscription pricing plans including quotas and account expiration.\n* [django-subscriptions](https://github.com/kogan/django-subscriptions) A django package for managing the status and terms of a subscription.\n* [django-paddle](https://github.com/kennell/django-paddle) Django models and helpers for integrating paddle subscriptions.\n* [dj-paddle](https://github.com/paddle-python/dj-paddle) for subscriptions-related paddle integration.\n",
    'author': 'Señor Rolando',
    'author_email': 'rolando@buechergefahr.de',
    'maintainer': 'Señor Rolando',
    'maintainer_email': 'rolando@buechergefahr.de',
    'url': 'https://codeberg.org/buechergefahr/dj-happy-quotas',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
