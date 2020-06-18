from lb_dev.constants import license_constants
import re


class CopyrightBuilder:

    def __init__(self):
        self.owner = '{owner}'
        self.year = '{year}'
        self.license_type = '{license_type}'
        self.license_file = '{license_file}'
        self.copyright = '''
(c) Copyright {year} {owner}

This software is distributed under the terms of the {license_type}, copied verbatim in the file "{license_file}".
'''

    def add_year(self, year):
        self.year = year

    def add_license_type(self, license_type):
        self.license_type = license_type

    def add_license_file(self, license_file):
        self.license_file = license_file

    def add_owner(self, owner):
        self.owner = owner

    def get_license(self):
        if self.license_type == 'mit':
            license_content = license_constants.mit_license
        elif self.license_type == 'apache-2.0':
            license_content = license_constants.apache2_license
        elif self.license_type == 'gpl-3.0':
            license_content = license_constants.gpl3_license
        else:
            print('The license you are trying to use is not currently supported')
            return '[invalid license] {}'.format(self.license_type)

        return license_content

    def build_copyright(self):
        copyright = self.copyright                                              \
                        .replace('{year}', str(self.year))                      \
                        .replace('{owner}', self.owner)                         \
                        .replace('{license_type}', self.get_license())          \
                        .replace('{license_file}', self.license_file).strip()

        if re.match(r'.+\sCERN(\s[a-zA-Z0-9\s,-]+)*\s*$', copyright.split('\n')[0]):
            copyright = '\n\n'.join([copyright, license_constants.PRIVILEGES_AND_IMMUNITIES_PARAGRAPH])
        
        return  copyright
