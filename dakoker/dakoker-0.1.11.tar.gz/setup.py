# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'fire>=0.3.1,<0.4.0',
 'ipython>=7.15.0,<8.0.0',
 'pendulum>=2.1.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'slackbot>=0.5.6,<0.6.0']

entry_points = \
{'console_scripts': ['dakoker = src.dakoker:main']}

setup_kwargs = {
    'name': 'dakoker',
    'version': '0.1.11',
    'description': '',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/dakoker.svg)](https://pypi.python.org/pypi/dakoker)\n\nMF-Dakoker\n=======\n\n[MFクラウド勤怠](https://biz.moneyforward.com/attendance)利用者向けに作った打刻・勤怠状況確認ツールです。\n\n主な機能\n- MFクラウド勤怠へのログイン, 出勤・退勤の打刻\n\n実装予定機能\n- 休憩時間の打刻\n- 二重打刻の防止機能\n- 過去・当日の勤怠状況の確認(打刻日時)\n\n動作環境\n- Python 3.8以降\n\n## How to Install\n`pip3 install dakoker`\n\n## Usage\n\n- 出勤\n  - `dakoker start`\n- 退勤\n  - `dakoker stop`\n\n### 初回利用時\nログインのため、以下の情報を入力します\n(2回目以降は前回ログイン時のcookieを読み込み自動ログインします)\n- 企業ID\n- ユーザーID もしくは登録メールアドレス\n- パスワード\n\n![初回ログイン時](https://gyazo.com/e0657a3eecfc6a486a469a0cebd98db1.png)\n',
    'author': 'nixiesquid',
    'author_email': 'audu817@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
