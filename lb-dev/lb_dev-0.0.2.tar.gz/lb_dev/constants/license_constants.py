###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import re

LICENSE_FILESNAMES = ['LICENSE', 'LICENCE',
                      'LICENSE.md', 'LICENSE.md', 'COPYING', 'COPYING.md']

LICENSE_REST_ENDPOINT = 'https://api.github.com/licenses/'

CHECKED_FILES = re.compile(
    r'.*(\.(i?[ch](pp|xx|c)?|cc|hh|py|C|cmake|[yx]ml|qm[ts]|dtd|xsd|ent|bat|[cz]?sh|js|html?)|'
    r'CMakeLists.txt|Jenkinsfile)$')

COPYRIGHT_SIGNATURE = re.compile(r'\bcopyright\b', re.I)

# see https://www.python.org/dev/peps/pep-0263 for the regex
ENCODING_DECLARATION = re.compile(
    r'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)')

gpl3_license = 'GNU General Public \nLicence version 3 (GPL Version 3)'

apache2_license = 'Apache License,\nVersion 2.0'

mit_license = 'MIT\nLicense'

PRIVILEGES_AND_IMMUNITIES_PARAGRAPH = '''
In applying this licence, CERN does not waive the privileges and immunities
granted to it by virtue of its status as an Intergovernmental Organization
or submit itself to any jurisdiction.
'''.strip()