# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ics_vtimezones']

package_data = \
{'': ['*'],
 'ics_vtimezones': ['data/*',
                    'data/zoneinfo/*',
                    'data/zoneinfo/Africa/*',
                    'data/zoneinfo/America/*',
                    'data/zoneinfo/America/Argentina/*',
                    'data/zoneinfo/America/Indiana/*',
                    'data/zoneinfo/America/Kentucky/*',
                    'data/zoneinfo/America/North_Dakota/*',
                    'data/zoneinfo/Antarctica/*',
                    'data/zoneinfo/Arctic/*',
                    'data/zoneinfo/Asia/*',
                    'data/zoneinfo/Atlantic/*',
                    'data/zoneinfo/Australia/*',
                    'data/zoneinfo/Brazil/*',
                    'data/zoneinfo/Canada/*',
                    'data/zoneinfo/Chile/*',
                    'data/zoneinfo/Etc/*',
                    'data/zoneinfo/Europe/*',
                    'data/zoneinfo/Indian/*',
                    'data/zoneinfo/Mexico/*',
                    'data/zoneinfo/Pacific/*',
                    'data/zoneinfo/US/*']}

install_requires = \
['importlib_resources>=1.4,<2.0']

extras_require = \
{'update': ['ics>=0.8.0,<0.9.0']}

setup_kwargs = {
    'name': 'ics-vtimezones',
    'version': '2020.1',
    'description': 'iCalendar vTimezone Data',
    'long_description': '# ics.py vTimezone Data\nThis project independently packages the timezone data required by [`ics.py`](https://github.com/C4ptainCrunch/ics.py).\nIt includes the [Olson / IANA timezone Database](https://www.iana.org/time-zones) converted to [iCalender vTimezone](https://icalendar.org/iCalendar-RFC-5545/3-6-5-time-zone-component.html) files by [vzic](https://github.com/libical/vzic/)\nand the [Unicode CLDR](http://cldr.unicode.org/index) mapping of [Windows timezone names](http://cldr.unicode.org/development/development-process/design-proposals/extended-windows-olson-zid-mapping) to the Olson identifiers.\n\nHaving a separate project from ics.py allows regular releases when the timezone data changes\n(which is not as seldom as you might think) without having to do a new release of `ics.py`.\nSimilar to `pytz`, this project follows the `YYYY.minor` [calendar versioning](https://calver.org/) scheme representing the periodic updates of its data,\nwhile `ics.py` uses [semantic versioning](https://semver.org/) to allow ensuring compatibility with its more gradually evolving code-base.\n\n## License\nThe source code of the project itself and the IANA time zone database are in the public domain,\nwhile the Unicode CLDR Windows timezone name mapping file is under the [Unicode, inc. license agreement for data files and software](https://www.unicode.org/license.html), having the following copyright notice:\n> Copyright © 1991-2013 Unicode, Inc.\n> CLDR data files are interpreted according to the LDML specification (http://unicode.org/reports/tr35/)\n> For terms of use, see http://www.unicode.org/copyright.html',
    'author': 'Niko Fink',
    'author_email': 'icspy@niko.fink.bayern',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/ics_vtimezones/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
