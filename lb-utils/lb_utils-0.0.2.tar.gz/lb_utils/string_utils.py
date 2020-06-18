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


class StringUtils:

    @staticmethod
    def find_strings_in_list(strings, string_list):
        """
        takes in as a parameter two lists of strings
        and returns the strings that appear in both lists

        :param strings: list[str, str..., str]
        
        :param string_list: list[str, str..., str]

        :return list[str, str..., str]
        """
        return [string for string in strings if string in string_list]

    @staticmethod
    def to_comment(text, lang_family='#', width=80):
        r'''
        Convert a chunk of text into comment for source files.

        The parameter lang_family can be used to tune the style of the comment:

            - 'c' for C/C++
            - '#' (default) for Python, shell, etc.
            - 'xml' for XML files

        >>> print(to_comment('a\nb\nc\n'), end='')
        ###############################################################################
        # a                                                                           #
        # b                                                                           #
        # c                                                                           #
        ###############################################################################
        >>> print(to_comment('a\nb\nc\n', 'c'), end='')
        /*****************************************************************************\
        * a                                                                           *
        * b                                                                           *
        * c                                                                           *
        \*****************************************************************************/
        >>> print(to_comment('a\nb\nc\n', 'xml'), end='')
        <!--
            a
            b
            c
        -->
        '''
        if lang_family == 'c':
            head = '/{}\\'.format((width - 3) * '*')
            line = '* {:%d} *' % (width - 5)
            tail = '\\{}/'.format((width - 3) * '*')
        elif lang_family in ('#', 'py'):
            head = (width - 1) * '#'
            line = '# {:%d} #' % (width - 5)
            tail = head
        elif lang_family == 'xml':
            head = '<!--'
            line = '    {}'
            tail = '-->'
        else:
            raise ValueError('invalid language family: {}'.format(lang_family))

        data = [head]
        data.extend(line.format(l.rstrip()).rstrip() for l in text.splitlines())
        data.append(tail)
        data.append('')
        return '\n'.join(data)

    @staticmethod
    def make_package_compatible(string):
        return string.replace('-', '_')