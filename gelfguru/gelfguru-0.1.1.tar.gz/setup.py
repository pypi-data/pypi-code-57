# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gelfguru']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'gelfguru',
    'version': '0.1.1',
    'description': 'Loguru extension for log in GELF payload format.',
    'long_description': '# loguru-gelf-extension\n\nA Loguru extension for handling log messages and adapt to GELF payload pattern, without modifying  built-in Loguru methods call.\n\nThis library was created especially for applications running in Docker environment with GELF Logging Driver.\n\nFeatures:\n    - Dont modify call methods Loguru, like `logger.trace`, `logger.info`, `logger.info` etc...;\n    - Create new methods for `logger` instace, with all [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity level;\n    - Associates [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity Levels Numerical Codes in GELF field.\n\n\n# Installation\n\n```shell\npip3.7 install gelfguru\n```\n\n\n# How to Use \n\nIf you configure loguru instance with `gelfguru`, you only need to execute:\n\n```python\nfrom loguru import logger\nfrom gelfguru import configure_gelf_output\n\nconfigure_gelf_output()\n\nlogger.trace(\'loguru trace calls equals gelfguru debug calls\')\nlogger.info(\'Change numeric level value, in the case, is used RFC-5424 numeric level value\')\nlogger.emergency(\'Implemented RFC-5424 Syslog Severity Logs\')\nlogger.emerg(\'Implemented RFC-5424 Keyword calls\')\n```\n\n\n## Log Levels\n\nGELF log level is equal to the standard syslog levels.\n\n\nValue |\tSeverity\t   | Keyword  | Description\n:---: |:---:           |:---:     | :---:\n0     | Emergency      |  emerg   | System is unusable. A panic condition\n1     | Alert          |  alert   | Action must be taken immediately. A condition that should be corrected immediately, such as a corrupted system database.[\n2     | Critical       |  crit    | Critical conditions. Hard device errors\n3     | Error          |  err     | Error conditions. \n4     | Warning        |  warning | Warning conditions\n5     | Notice         |  notice  | Normal but significant condition. Conditions that are not error conditions, but that may require special handling\n6     | Informational  |  info    | Informational messages\n7     | Debug          |  debug   | Debug-level messages. Messages that contain information normally of use only when debugging a program.\n\n\ngelfguru implements methods with Severity or Keyword, for example:\n\n```python\n>>> import logger\n>>> from gelfguru import configure_gelf_output \n\n>>> configure_gelf_output() \n\n>>> logger.bind(field_extra=\'any_field\').trace(\'Extra fields add with .bind() function\')\n\n{\n  "version": "1.1",\n  "short_message": "Extra fields add with .bind() function",\n  "full_message": "TRACE\\n",\n  "timestamp": 1593051186.92822,\n  "level": 5,\n  "line": 6,\n  "_file": "/home/augustoliks/github/loguru-gelf-extension/test.py",\n  "_context": {\n    "module": "__main__:<module>:6",\n    "process": "MainProcess",\n    "thread": "MainThread"\n  },\n  "_field_extra": "any_field"\n}\n\n>>> logger.bind(id=\'6sdaf4das6f34453\').info(\'id bind is trasform to _id_record\')\n\n{\n  "version": "1.1",\n  "short_message": "id bind is trasform to _id_record",\n  "full_message": "info\\n",\n  "timestamp": 1593051186.929191,\n  "level": 6,\n  "line": 7,\n  "_file": "/home/augustoliks/github/loguru-gelf-extension/test.py",\n  "_context": {\n    "module": "__main__:<module>:7",\n    "process": "MainProcess",\n    "thread": "MainThread"\n  },\n  "_id_record": "6sdaf4das6f34453"\n}\n```\n',
    'author': 'Carlos Neto',
    'author_email': 'carlos.santos110@fatec.sp.gov.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
