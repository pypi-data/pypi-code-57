# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pytime_converter', 'pytime_converter.helper']

package_data = \
{'': ['*'], 'pytime_converter': ['service/*']}

setup_kwargs = {
    'name': 'pytime-converter',
    'version': '0.1.7',
    'description': 'Easily convert differt time-range format to standard ones',
    'long_description': "![codecov](https://codecov.io/gh/massicer/Env-Time-Converter/branch/master/graph/badge.svg)\n[![Build Status](https://travis-ci.org/massicer/PyTime-Converter.svg?branch=master)](https://travis-ci.org/massicer/PyTime-Converter)\n\n# PyTime Converter\n\nEasily manage different `time interval values` and convert them to `milliseconds`.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.\n\n### Prerequisites\n\n- [Poetry >=0.12](https://python-poetry.org)\n- Python ^3.5\n- Virtualenvwrapper or other virtualenv environment\n- make utility\n\n### Installing\n\nClone or download the repository\n\n```\ngit clone https://github.com/massicer/Env-Time-Converter.git\n```\n\nInstall project package\n```\nmake install\n```\n\nor without the make utility\n```\npoetry install\n```\n## Running the tests\n\nSimply type\n```\nmake test\n```\n## How To use\n\n### Available time formats\n| Unit Measure       | Allowed Sigles | default |\n| ------------- |:-----:| :-----:|\n| `milliseconds`  | `ms` , `milliseconds`, `sec`| `X`\n| `seconds`  | `seconds` , `s`, `sec`|\n| `minutes`  | `min` , `minute`, `minutes`|\n| `hours`  | `h` , `hours`, `hrs`, `hour`|\n| `days`  | `d` , `days`, `day`|\n| `years`  | `y` , `years`, `yrs`, `year`|\n\n\n\n - Simply using the `get_milliseconds_value_for_input` with the string value to convert. The below example use the number value `90` and the sigle `s`. \n \n    ```\n    from pytime_converter.service.convert_service import get_milliseconds_value_for_input\n    \n    # Assume this ENV is set by your .yaml or other configuration file.\n    job_time =  '90 seconds' \n\n    assert 9000 == get_milliseconds_value_for_input(job_time)\n    ```\n\n- When the time measure unit is missing the default value is `milliseconds`\n\n    ```\n    from pytime_converter.service.convert_service import get_milliseconds_value_for_input\n    \n    assert 90 == get_milliseconds_value_for_input('90')\n    ```\n\n\n## Authors\n\n* **[Massimiliano Ceriani](massimilianoceriani08@gmail.com)** - *Initial work* - [ENV Time Converter](https://github.com/massicer/Env-Time-Converter)\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n",
    'author': 'Massimiliano Ceriani',
    'author_email': 'massimiliano.ceriani08@gmail.com',
    'url': 'https://github.com/massicer/PyTime-Converter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
