# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indexpy', 'indexpy.http', 'indexpy.openapi', 'indexpy.websocket']

package_data = \
{'': ['*']}

install_requires = \
['a2wsgi>=0.3.5,<0.4.0',
 'aiofiles>=0.5.0,<0.6.0',
 'jinja2>=2.10.3,<3.0.0',
 'pydantic>=1.5,<2.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.3,<6.0',
 'starlette>=0.13.1,<0.14.0',
 'uvicorn>=0.11.3,<0.12.0',
 'watchdog>=0.10.2,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0'],
 'gunicorn': ['gunicorn>=20.0.4,<21.0.0'],
 'pytest': ['pytest>=5.4.2,<6.0.0'],
 'requests': ['requests>=2.23.0,<3.0.0'],
 'test': ['requests>=2.23.0,<3.0.0', 'pytest>=5.4.2,<6.0.0']}

entry_points = \
{'console_scripts': ['index-cli = indexpy.cli:main']}

setup_kwargs = {
    'name': 'index.py',
    'version': '0.10.8',
    'description': 'An easy-to-use asynchronous web framework based on ASGI.',
    'long_description': '# index.py\n\n[![Github Action Test](https://github.com/abersheeran/index.py/workflows/Test/badge.svg)](https://github.com/abersheeran/index.py/actions?query=workflow%3ATest)\n[![PyPI](https://img.shields.io/pypi/v/index.py)](https://pypi.org/project/index.py/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/index.py)\n\n一个基于 ASGI 协议的高性能 web 框架。[Index.py 文档](https://abersheeran.github.io/index.py/)\n\n你也可以直接查看 [Example](https://github.com/abersheeran/index.py/tree/master/example) 来学习如何使用（文档偶尔会滞后一到两天，但 example 被纳入了自动化测试，所以会始终保持最新版）\n\n- 无需手动绑定路由 (文件系统映射URI)\n- 自动解析请求 & 生成文档 (基于 pydantic)\n- 可视化 API 接口 (基于 ReDoc, 针对中文字体优化)\n- 现代化的测试组件 (基于 pytest 与 requests)\n- 非常简单的部署 (基于 uvicorn 与 gunicorn)\n- 支持真正的热重载\n- 挂载 ASGI/WSGI 应用 (比 starlette 更易用)\n- 更好用的 background tasks\n- 可使用任何可用的 ASGI 生态\n\n## Install\n\n```bash\npip install -U index.py\n```\n\n或者直接从 Github 上安装最新版本（不稳定）\n\n```bash\npip install -U git+https://github.com/abersheeran/index.py\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/index.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
