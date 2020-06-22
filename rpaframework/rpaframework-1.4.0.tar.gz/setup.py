# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA',
 'RPA.Cloud',
 'RPA.Desktop',
 'RPA.Email',
 'RPA.Excel',
 'RPA.Outlook',
 'RPA.Robocloud',
 'RPA.Word',
 'RPA.core']

package_data = \
{'': ['*']}

install_requires = \
['clipboard>=0.0.4,<0.0.5',
 'exchangelib>=3.1.1,<4.0.0',
 'fpdf>=1.7.2,<2.0.0',
 'graphviz>=0.13.2,<0.14.0',
 'netsuitesdk>=1.1.0,<2.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pdfminer.six>=20200402,<20200403',
 'pillow>=7.0.0,<8.0.0',
 'pypdf2>=1.26.0,<2.0.0',
 'pyscreenshot>=1.0,<2.0',
 'robotframework-databaselibrary>=1.2.4,<2.0.0',
 'robotframework-requests>=0.6.5,<0.7.0',
 'robotframework-seleniumlibrary>=4.1.0,<5.0.0',
 'robotframework-seleniumtestability>=0.9.2,<0.10.0',
 'robotframework>=3.2.1,<4.0.0',
 'simple_salesforce>=1.0.0,<2.0.0',
 'tweepy>=3.8.0,<4.0.0',
 'webdrivermanager>=0.7.4',
 'xlrd>=1.2.0,<2.0.0',
 'xlutils>=2.0.0,<3.0.0',
 'xlwt>=1.3.0,<2.0.0']

extras_require = \
{':python_version < "3.7.6" and sys_platform == "win32" or python_version > "3.7.6" and python_version < "3.8.1" and sys_platform == "win32" or python_version > "3.8.1" and sys_platform == "win32"': ['pywinauto>=0.6.8,<0.7.0',
                                                                                                                                                                                                        'pywin32>=227,<228'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 ':sys_platform == "win32"': ['robotframework-sapguilibrary>=1.1,<2.0',
                              'psutil>=5.7.0,<6.0.0'],
 'aws': ['boto3>=1.13.4,<2.0.0'],
 'cv': ['opencv-python>=4.2.0,<5.0.0', 'numpy>=1.18.2,<2.0.0'],
 'google': ['google-cloud-vision>=1.0.0,<2.0.0',
            'google-cloud-language>=1.3.0,<2.0.0',
            'google-cloud-videointelligence>=1.14.0,<2.0.0',
            'google-cloud-translate>=2.0.1,<3.0.0',
            'google-cloud-texttospeech>=1.0.1,<2.0.0',
            'google-cloud-speech>=1.3.2,<2.0.0',
            'google-cloud-storage>=1.28.1,<2.0.0',
            'grpcio>=1.29.0,<2.0.0']}

setup_kwargs = {
    'name': 'rpaframework',
    'version': '1.4.0',
    'description': 'A collection of tools and libraries for RPA',
    'long_description': 'RPA Framework\n=============\n\n.. contents:: Table of Contents\n   :local:\n   :depth: 1\n\n.. include-marker\n\nIntroduction\n------------\n\n`RPA Framework` is a collection of open-source libraries and tools for\nRobotic Process Automation (RPA), and it is designed to be used with both\n`Robot Framework`_ and Python_. The goal is to offer well-documented and\nactively maintained core libraries for Software Robot Developers.\n\nLearn more about RPA at Robohub_.\n\n**The project is:**\n\n- 100% Open Source\n- Sponsored by Robocorp_\n- Optimized for Robocloud_ and Robocode_\n- Accepting external contributions\n\n.. _Robot Framework: https://robotframework.org\n.. _Robot Framework Foundation: https://robotframework.org/foundation/\n.. _Python: https://python.org\n.. _Robohub: https://hub.robocorp.com\n.. _Robocorp: https://robocorp.com\n.. _Robocloud: https://hub.robocorp.com/introduction/robocorp-suite/robocloud/\n.. _Robocode: https://hub.robocorp.com/introduction/robocorp-suite/robocode-lab/\n\nLinks\n^^^^^\n\n- Homepage: `<https://www.github.com/robocorp/rpaframework/>`_\n- Documentation: `<https://rpaframework.org/>`_\n- PyPI: `<https://pypi.org/project/rpaframework/>`_\n\n------------\n\n.. image:: https://github.com/robocorp/rpaframework/workflows/main/badge.svg\n   :target: https://github.com/robocorp/rpaframework/actions?query=workflow%3Amain\n   :alt: Status\n\n.. image:: https://img.shields.io/pypi/v/rpaframework.svg?label=version\n   :target: https://pypi.python.org/pypi/rpaframework\n   :alt: Latest version\n\n.. image:: https://img.shields.io/pypi/l/rpaframework.svg\n   :target: http://www.apache.org/licenses/LICENSE-2.0.html\n   :alt: License\n\n\nLibraries\n---------\n\nThe RPA Framework project currently includes the following libraries:\n\n+----------------------------+----------------------------------------------+\n| `Browser`_                 | Control browsers and automate the web        |\n+----------------------------+----------------------------------------------+\n| `Cloud.AWS`_               | Use Amazon AWS services                      |\n+----------------------------+----------------------------------------------+\n| `Cloud.Azure`_             | Use Microsoft Azure services                 |\n+----------------------------+----------------------------------------------+\n| `Cloud.Google`_            | Use Google Cloud services                    |\n+----------------------------+----------------------------------------------+\n| `Database`_                | Interact with databases                      |\n+----------------------------+----------------------------------------------+\n| `Desktop.Clipboard`_       | Interact with the system clipboard           |\n+----------------------------+----------------------------------------------+\n| `Desktop.OperatingSystem`_ | Read OS information and manipulate processes |\n+----------------------------+----------------------------------------------+\n| `Desktop.Windows`_         | Automate Windows desktop applications        |\n+----------------------------+----------------------------------------------+\n| `Email.Exchange`_          | E-Mail operations (Exchange protocol)        |\n+----------------------------+----------------------------------------------+\n| `Email.ImapSmtp`_          | E-Mail operations (IMAP & SMTP)              |\n+----------------------------+----------------------------------------------+\n| `Excel.Application`_       | Control the Excel desktop application        |\n+----------------------------+----------------------------------------------+\n| `Excel.Files`_             | Manipulate Excel files directly              |\n+----------------------------+----------------------------------------------+\n| `FileSystem`_              | Read and manipulate files and paths          |\n+----------------------------+----------------------------------------------+\n| `HTTP`_                    | Interact directly with web APIs              |\n+----------------------------+----------------------------------------------+\n| `Images`_                  | Manipulate images                            |\n+----------------------------+----------------------------------------------+\n| `Outlook.Application`_     | Control the Outlook desktop application      |\n+----------------------------+----------------------------------------------+\n| `PDF`_                     | Read and create PDF documents                |\n+----------------------------+----------------------------------------------+\n| `Robocloud.Items`_         | Use the Robocloud Work Items API             |\n+----------------------------+----------------------------------------------+\n| `Robocloud.Secrets`_       | Use the Robocloud Secrets API                |\n+----------------------------+----------------------------------------------+\n| `Salesforce`_              | Salesforce operations                        |\n+----------------------------+----------------------------------------------+\n| `SAP`_                     | Control SAP GUI desktop client               |\n+----------------------------+----------------------------------------------+\n| `Slack`_                   | Send notifications to Slack channels         |\n+----------------------------+----------------------------------------------+\n| `Tables`_                  | Manipulate, sort, and filter tabular data    |\n+----------------------------+----------------------------------------------+\n| `Tasks`_                   | Control task execution                       |\n+----------------------------+----------------------------------------------+\n| `Twitter`_                 | Twitter API interface                        |\n+----------------------------+----------------------------------------------+\n| `Word.Application`_        | Control the Word desktop application         |\n+----------------------------+----------------------------------------------+\n\n.. _Browser: https://rpaframework.org/libraries/browser/\n.. _Cloud.AWS: https://rpaframework.org/libraries/cloud_aws/\n.. _Cloud.Azure: https://rpaframework.org/libraries/cloud_azure/\n.. _Cloud.Google: https://rpaframework.org/libraries/cloud_google/\n.. _Database: https://rpaframework.org/libraries/database/\n.. _Desktop.Clipboard: https://rpaframework.org/libraries/desktop_clipboard/\n.. _Desktop.Operatingsystem: https://rpaframework.org/libraries/desktop_operatingsystem/\n.. _Desktop.Windows: https://rpaframework.org/libraries/desktop_windows/\n.. _Email.Exchange: https://rpaframework.org/libraries/email_exchange/\n.. _Email.ImapSmtp: https://rpaframework.org/libraries/email_imapsmtp/\n.. _Excel.Application: https://rpaframework.org/libraries/excel_application/\n.. _Excel.Files: https://rpaframework.org/libraries/excel_files/\n.. _FileSystem: https://rpaframework.org/libraries/filesystem/\n.. _HTTP: https://rpaframework.org/libraries/http/\n.. _Images: https://rpaframework.org/libraries/images/\n.. _Outlook.Application: https://rpaframework.org/libraries/outlook_application/\n.. _PDF: https://rpaframework.org/libraries/pdf/\n.. _Robocloud.Items: https://rpaframework.org/libraries/robocloud_items/\n.. _Robocloud.Secrets: https://rpaframework.org/libraries/robocloud_secrets/\n.. _Salesforce: https://rpaframework.org/libraries/salesforce/\n.. _SAP: https://rpaframework.org/libraries/sap/\n.. _Slack: https://rpaframework.org/libraries/slack/\n.. _Tables: https://rpaframework.org/libraries/tables/\n.. _Tasks: https://rpaframework.org/libraries/tasks/\n.. _Twitter: https://rpaframework.org/libraries/twitter/\n.. _Word.Application: https://rpaframework.org/libraries/word_application/\n\n\nInstallation\n------------\n\nIf you already have Python_ and `pip <http://pip-installer.org>`_ installed,\nyou can use:\n\n``pip install rpaframework``\n\n.. note:: Python 3.6 or higher is required\n\nExample\n-------\n\nAfter installation the libraries can be directly imported inside\n`Robot Framework`_:\n\n.. code:: robotframework\n\n    *** Settings ***\n    Library    RPA.Browser\n\n    *** Tasks ***\n    Login as user\n        Open browser  https://example.com\n        Input text    id:user-name    ${USERNAME}\n        Input text    id:password     ${PASSWORD}\n\nThe libraries are also available inside Python_:\n\n.. code:: python\n\n    from RPA.Browser import Browser\n\n    lib = Browser()\n\n    lib.open_browser("https://example.com")\n    lib.input_text("id:user-name", username)\n    lib.input_text("id:password", password)\n\nSupport and contact\n-------------------\n\n- `rpaframework.org <https://rpaframework.org/>`_ for library documentation\n- Robohub_ for guides and tutorials\n- **#rpaframework** channel in `Robot Framework Slack`_ if you\n  have open questions or want to contribute\n\n.. _Robot Framework Slack: https://robotframework-slack-invite.herokuapp.com/\n\nContributing\n------------\n\nFound a bug? Missing a critical feature? Interested in contributing?\nHead over to the `Contribution guide <https://rpaframework.org/contributing/guide.html>`_\nto see where to get started.\n\nLicense\n-------\n\nThis project is open-source and licensed under the terms of the\n`Apache License 2.0 <http://apache.org/licenses/LICENSE-2.0>`_.\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
