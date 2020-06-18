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
from lb_utils.string_utils import StringUtils
from pytest import raises

def test_find_strings_in_list():
    strings = ["string1", "string2"]
    list_items = ["item1", {}, "string1", "item3"]

    strings_in_list = StringUtils.find_strings_in_list(strings, list_items)

    assert ["string1"] == strings_in_list


def test_find_strings_in_empty_list():
    strings = ["string1", "string2"]
    list_items = []

    strings_in_list = StringUtils.find_strings_in_list(strings, list_items)

    assert [] == strings_in_list

def test_to_comment_python():
    expected_result = '''
###############################################################################
# a                                                                           #
# b                                                                           #
# c                                                                           #
###############################################################################
'''
    
    assert expected_result.strip() == StringUtils.to_comment('a\nb\nc').strip()

def test_to_comment_c():
    expected_result = '''
/*****************************************************************************\\
* a                                                                           *
* b                                                                           *
* c                                                                           *
\*****************************************************************************/
'''
    
    assert expected_result.strip() == StringUtils.to_comment('a\nb\nc', 'c').strip()

def test_to_comment_xml():
    expected_result = '''
<!--
    a
    b
    c
-->
'''
    
    assert expected_result.strip() == StringUtils.to_comment('a\nb\nc', 'xml').strip()

def test_to_comment_random_language():
    
    with raises(ValueError):
        assert StringUtils.to_comment('a\nb\nc', 'perl')

def test_make_package_compatible():
    string = 'some-string'

    assert 'some_string' == StringUtils.make_package_compatible(string)