import re

class CopyrightScanner:

    comment_block_start_pattern = r'^(/(\*)+\\|#+|<!--)\s*$'
    comment_block_end_pattern = r'^(\\(\*)+/|#+|-->)\s*$'
    copyright_first_line_pattern = r'^([#\*]{0,1})\s(\(c\)\sCopyright\s([0-9]{4}(-[0-9]{4}){0,1})\s([a-zA-Z0-9\s,-]+))\s\1$'
    copyright_year_pattern = r'\s([0-9]{4}(-[0-9]{4}){0,1})\s'
    license_type_pattern = r'Apache|MIT|GNU'
    license_file_pattern = r'"([a-zA-Z]+(\.[a-zA-Z]+)*)"'

    def __init__(self):
        self.file_path = ''
        self.copyright_statement_start = 0
        self.copyright_statement_end = 0
        self.copyright_statement_lines = []

    def set_file_path(self, file_path):
        self.file_path = file_path

    def extract_copyright_statement(self):
        self.copyright_statement_lines = []
        is_inside_copyright = False
        with open(self.file_path) as file:
            for i, line in enumerate(file):
                if re.match(self.comment_block_start_pattern, line):
                    if is_inside_copyright:
                        self.copyright_statement_end = i
                        self.copyright_statement_lines.append(line)
                        break
                    else:
                        self.copyright_statement_start = i
                        self.copyright_statement_lines.append(line)
                        is_inside_copyright = True
                elif is_inside_copyright:
                    self.copyright_statement_lines.append(line)
                    if re.match(self.comment_block_end_pattern, line):
                        self.copyright_statement_end = i
                        break
                    
                    
        return self.copyright_statement_lines, self.copyright_statement_start, self.copyright_statement_end

    def extract_owner(self):
        if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
            self.extract_copyright_statement()
            if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
                raise ValueError('File does not have a copyright statement')

        for line in self.copyright_statement_lines:
            first_line_search = re.search(self.copyright_first_line_pattern, line)
            if first_line_search:
                owner = first_line_search.group(5)
                return owner.strip()

    def extract_copyright_year(self):
        if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
            self.extract_copyright_statement()
            if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
                raise ValueError('File does not have a copyright statement')

        for line in self.copyright_statement_lines:
            first_line_search = re.search(self.copyright_first_line_pattern, line)
            if first_line_search:
                year_search = re.search(self.copyright_year_pattern, first_line_search.group(0))
                if year_search:
                    year = year_search.group(1)
                    return year

    def extract_license_type(self):
        if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
            self.extract_copyright_statement()
            if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
                raise ValueError('File does not have a copyright statement')

        for line in self.copyright_statement_lines:
            license_type = self.extract_license_from_line(line)
            if license_type != '':
                return license_type

        raise ValueError('Not supported license')

    def extract_license_from_line(self, line):
        license_type_search = re.search(self.license_type_pattern, line)
        if license_type_search:
            if license_type_search.group(0) == 'Apache':
                return 'apache-2.0'
            elif license_type_search.group(0) == 'MIT':
                return 'mit'
            elif license_type_search.group(0) == 'GNU':
                return 'gpl-3.0'
        else:
            return ''

    def extract_license_file_name(self):
        if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
            self.extract_copyright_statement()
            if self.copyright_statement_start == 0 and self.copyright_statement_end == 0 and self.copyright_statement_lines == []:
                raise ValueError('File does not have a copyright statement')

        for line in self.copyright_statement_lines:
            license_file_search = re.search(self.license_file_pattern, line)
            if license_file_search:
                license_file_name = license_file_search.group(1)

                return license_file_name