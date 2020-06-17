# -*- coding: utf-8 -*-
"""
test module for merging video files
"""

import unittest.mock as mock

from sail_utils.cv.merge import Merger


class _MockedOSSUtil:

    def __init__(self):
        pass


def test_merger_download_files():
    """
    test merger's download files utils
    :return:
    """
    merge = Merger(company_id=1,
                   shop_id=1,
                   ipc_id=1,
                   oss_utils=_MockedOSSUtil())
    merge.oss_utils.list = mock.Mock(return_value=['100_121.flv',
                                                   '122_156.flv',
                                                   '183_195.flv',
                                                   '230_240.flv',
                                                   '243_296.flv'])
    merge.oss_utils.download = mock.Mock()
    calculated = merge.download_files(123, 235)
    expected = ['tmp/122_156.flv', 'tmp/183_195.flv', 'tmp/230_240.flv']
    for cal, exp in zip(calculated, expected):
        assert cal.as_posix() == exp
