# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_powertools',
 'aws_lambda_powertools.logging',
 'aws_lambda_powertools.metrics',
 'aws_lambda_powertools.middleware_factory',
 'aws_lambda_powertools.tracing']

package_data = \
{'': ['*']}

install_requires = \
['aws-xray-sdk>=2.5.0,<2.6.0', 'fastjsonschema>=2.14.4,<2.15.0']

setup_kwargs = {
    'name': 'aws-lambda-powertools',
    'version': '1.0.0',
    'description': 'Python utilities for AWS Lambda functions including but not limited to tracing, logging and custom metric',
    'long_description': '# Lambda Powertools\n\n![Build](https://github.com/awslabs/aws-lambda-powertools/workflows/Powertools%20Python/badge.svg?branch=master)\n![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.6%20|%203.7|%203.8&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/aws-lambda-powertools.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/aws-lambda-powertools)\n\nA suite of utilities for AWS Lambda Functions that makes tracing with AWS X-Ray, structured logging and creating custom metrics asynchronously easier.\n\n**[📜Documentation](https://awslabs.github.io/aws-lambda-powertools-python/)** | **[API Docs](https://awslabs.github.io/aws-lambda-powertools-python/api/)** | **[🐍PyPi](https://pypi.org/project/aws-lambda-powertools/)** | **[Feature request](https://github.com/awslabs/aws-lambda-powertools-python/issues/new?assignees=&labels=feature-request%2C+triage&template=feature_request.md&title=)** | **[🐛Bug Report](https://github.com/awslabs/aws-lambda-powertools-python/issues/new?assignees=&labels=bug%2C+triage&template=bug_report.md&title=)** | **[Kitchen sink example](https://github.com/awslabs/aws-lambda-powertools-python/tree/develop/example)**\n\n## Features\n\n* **[Tracing](https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/)** - Decorators and utilities to trace Lambda function handlers, and both synchronous and asynchronous functions\n* **[Logging](https://awslabs.github.io/aws-lambda-powertools-python/core/logger/)** - Structured logging made easier, and decorator to enrich structured logging with key Lambda context details\n* **[Metrics](https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/)** - Custom Metrics created asynchronously via CloudWatch Embedded Metric Format (EMF)\n* **[Bring your own middleware](https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/)** - Decorator factory to create your own middleware to run logic before, and after each Lambda invocation\n\n### Installation\n\nWith [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install aws-lambda-powertools``\n\n## Example\n\nSee **[example](./example/README.md)** of all features, testing, and a SAM template with all Powertools env vars. All features also provide full docs, and code completion for VSCode and PyCharm.\n\n## Credits\n\n* Structured logging initial implementation from [aws-lambda-logging](https://gitlab.com/hadrien/aws_lambda_logging)\n* Powertools idea [DAZN Powertools](https://github.com/getndazn/dazn-lambda-powertools/)\n* [Gatsby Apollo Theme for Docs](https://github.com/apollographql/gatsby-theme-apollo/tree/master/packages/gatsby-theme-apollo-docs)\n\n## License\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n',
    'author': 'Amazon Web Services',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/awslabs/aws-lambda-powertools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
