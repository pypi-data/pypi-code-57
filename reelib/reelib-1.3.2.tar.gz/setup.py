# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reelib']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.3,<2.0.0', 'opencv-python>=4.2.0,<5.0.0', 'pillow>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'reelib',
    'version': '1.3.2',
    'description': '頻繁に利用する処理を集めたライブラリ',
    'long_description': '# reelib\n\n頻繁に利用する処理を集めたライブラリ\n\n## インストール方法\n\n```sh\npip install reelib\n```\n\n## ライブラリの内容\n\n### timestamp\n\n- 時刻文字列を扱う\n\n```python\nfrom reelib import timestamp\n\n# 現在時刻のタイムスタンプを取得\nts = timestamp.get_timestamp()\n# ex) 20191025164844890916\n\n# タイムスタンプをdatetimeに変換\nt = timestamp.conv_time_from_timestamp(ts)\n# ex) datetime.datetime(2019, 10, 25, 16, 48, 44, 890916, tzinfo=datetime.timezone(datetime.timedelta(0, 32400)))\n```\n\n### contjson\n\n- JSONを扱う\n\n```python\nfrom reelib import contjson\n\n# ファイルからの読み込み\njson_obj = load_from_file(\'test.json\')\n\n# ファイルへの書き込み\nsave_to_file(json_obj, \'test.json\')\n\n# JSONを整形して標準出力\nprint_json(json_obj)\n\n# str型文字列をJSONに変換\njson_obj = json_from_str(\'{"a":2, "b":3}\')\n\n# JSONをstr型文字列に変換\njson_text = json_to_str(json_obj)\n```\n\n### contimg\n\n- 画像ファイルを扱う\n\n```python\nfrom reelib import contimg\n\n# PIL型をOpenCV型に変換\nimg_cv = contimg.pil2cv(img_pil)\n\n# OpenCV型をPIL型に変換\nimg_pil = contimg.cv2pil(img_cv)\n\n# 画像のリサイズ (トリミング)\nresized = contimg.resize(img_cv, (画像のサイズ(x,yのtuple)), fill=False)\n\n# 画像のリサイズ (パディング)\nresized = contimg.resize(img_cv, (画像のサイズ(x,yのtuple)), fill=True)\n\n# 画像タイルの作成\nimg_tile = contimg.get_imagetile((画像パスのリスト), (タイルのサイズ(x,yのtuple)), (タイルの数(x,yのtuple)))\n```\n',
    'author': 'reeve0930',
    'author_email': 'reeve0930@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reeve0930/reelib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
