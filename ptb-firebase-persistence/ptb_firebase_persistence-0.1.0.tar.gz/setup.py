# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptb_firebase_persistence']

package_data = \
{'': ['*']}

install_requires = \
['firebase-admin>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'ptb-firebase-persistence',
    'version': '0.1.0',
    'description': '',
    'long_description': '![](https://github.com/python-telegram-bot/logos/blob/master/logo/png/ptb-logo_240.png?raw=true)\n# Firebase Persistence for [python-telegram-bot](https://python-telegram-bot.org/)\n\nThis is an implementation of python-telegram-bot [BasePersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html?highlight=basepersistence) \nclass that uses [Google Firebase](https://firebase.google.com/) as persistence back-end. \nThis has a very nice advantage of being able to look at your `user_data`, `chat_data`, `bot_data` \nand `convesations` real-time using the firebase web app.\n\n# Installation\n\n\n# Usage\n\n## Before you start: obtain credentials from firebase\nFirst of all you need to obtain firebase credentials, that look like this:\n\n```json\n{\n  "type": "service_account",\n  "project_id": "YOUR_ID",\n  "private_key_id": "YOUR_PRIVATE_KEY",\n  "private_key": "-----BEGIN PRIVATE KEY-----\\nMII...EwQ=\\n-----END PRIVATE KEY-----\\n",\n  "client_email": "firebase-adminsdk-odh1e@SOME_DOMAIN.iam.gserviceaccount.com",\n  "client_id": "11743776666698009",\n  "auth_uri": "https://accounts.google.com/o/oauth2/auth",\n  "token_uri": "https://oauth2.googleapis.com/token",\n  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",\n  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-SOMES_STRING.iam.gserviceaccount.com"\n}\n```\n\nand the firebase database url that looks like this, something like `https://YOUR_APP.firebaseio.com`\n\n## Instantiation\n\n### From environment variables (recommended)\nStore the database URL in an environment variable `FIREBASE_URL` and the config as a json string in an environment variable\n`FIREBASE_CREDENTIALS`.\n\nAfter that instantiation is as easy as:\n\n```python\nfrom ptb_firebase_persistence import FirebasePersistence\nfrom telegram.ext import Updater\n\n\npersistence = FirebasePersistence.from_environment()\n\nupdater: Updater = Updater(\n    \'BOT_TOKEN\',\n    persistence=my_persistence,\n    use_context=True,\n)\n```\n\n### Direct instantiation\nYou can also just pass the firebase credentials as URL as simple init params:\n\n```python\nfrom ptb_firebase_persistence import FirebasePersistence\nfrom telegram.ext import Updater\n\n\npersistence = FirebasePersistence(database_url=\'YOUR_DATABASE_URL\', credentials=\'YOUR_CREDENTIALS_DICT\')\n\nupdater: Updater = Updater(\n    \'BOT_TOKEN\',\n    persistence=my_persistence,\n    use_context=True,\n)\n```\n',
    'author': 'Mikhail Beliansky',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
