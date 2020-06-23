# -*- coding: utf-8 -*-
import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

long_description = """
# Yandex.Checkout API Python Client Library

[![Build Status](https://travis-ci.org/yandex-money/yandex-checkout-sdk-python.svg?branch=master)](https://travis-ci.org/yandex-money/yandex-checkout-sdk-python)
[![Latest Stable Version](https://img.shields.io/pypi/v/yandex-checkout.svg)](https://pypi.org/project/yandex-checkout/)
[![Total Downloads](https://img.shields.io/pypi/dm/yandex-checkout.svg)](https://pypi.org/project/yandex-checkout/)
[![License](https://img.shields.io/pypi/l/yandex-checkout.svg)](https://github.com/yandex-money/yandex-checkout-sdk-python)

[Russian](https://github.com/yandex-money/yandex-checkout-sdk-python/blob/master/README.md) | English

This product is used for managing payments under [The Yandex.Checkout API](https://kassa.yandex.ru/docs/checkout-api/)
For usage by those who implemented Yandex.Checkout using the API method.

## Requirements
1. Python 2.7 or Python 3.x
2. pip

## Installation
### Under console using pip

1. Install pip.
2. In the console, run the following command:
```bash
pip install --upgrade yandex_checkout
```

### Under console using easy_install
1. Install easy_install.
2. In the console, run the following command:
```bash
easy_install --upgrade yandex_checkout
```

### Manually

1. In the console, run the following command:
```bash
wget https://pypi.python.org/packages/5a/be/5eafdfb14aa6f32107e9feb6514ca1ad3fe56f8e5ee59d20693b32f7e79f/yandex_checkout-1.0.0.tar.gz#md5=46595279b5578fd82a199bfd4cd51db2
tar zxf yandex_checkout-1.0.0.tar.gz
cd yandex_checkout-1.0.0
python setup.py install
```


## Commencing work

1. Import module
```python
import yandex_checkout
```

2. Configure a Client
```python
from yandex_checkout import Configuration

Configuration.configure('<Account Id>', '<Secret Key>')
```

or

```python
from yandex_checkout import Configuration

Configuration.account_id = '<Account Id>'
Configuration.secret_key = '<Secret Key>'
```

or via oauth

```python
from yandex_checkout import Configuration

Configuration.configure_auth_token('<Oauth Token>')
```

If you agree to participate in the development of the SDK, you can submit data about your framework, cms or module:

```python
from yandex_checkout import Configuration
from yandex_checkout.domain.common.user_agent import Version

Configuration.configure('<Account Id>', '<Secret Key>')
Configuration.configure_user_agent(
    framework=Version('Django', '2.2.3'),
    cms=Version('Wagtail', '2.6.2'),
    module=Version('Y.CMS', '0.0.1')
)
```

3. Call the required API method. [More details in our documentation for the Yandex.Checkout API](url)
"""


with open('yandex_checkout/__init__.py') as fp:
    version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

setup(
    name="yandex-checkout",
    version=version,
    description="Yandex Checkout SDK Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yandex-money/yandex-checkout-sdk-python",
    author="Yandex.Money",
    packages=find_packages('.', ['test']),
    install_requires=["requests", "uuid", "urllib3", 'distro'],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)
