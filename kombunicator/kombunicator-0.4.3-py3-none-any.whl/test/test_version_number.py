#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 19.06.20
@author: eisenmenger
"""
import pytest

from kombunicator.utils import get_version


@pytest.fixture(scope="module")
def release_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp('info').join('test_release_info')
    with open(fn, 'w') as file:
        file.write('VERSION_RELEASE=4.5.6\n')
        file.write('DEPLOY_VERSION=1.1.1\n')
        file.write('RELEASE_VERSION=2.32.97')
    return fn


dummy_data = [('RELEASE_VERSION', '2.32.97'), ('DEPLOY_VERSION', '1.1.1'), ('VERSION_RELEASE', '4.5.6')]


@pytest.mark.parametrize('version_string, expected', dummy_data)
def test_version_number(release_file, version_string, expected):
    assert get_version(file_name=release_file, version_string=version_string) == expected


def test_existing_release_info():
    assert get_version(file_name='release_info', version_string='RELEASE_VERSION') != '0.0.1'
