# -*- coding: utf-8 -*-
"""
test module for detection
"""

from sail_utils.cv.head.detection import _Mapper


def test_mapper():
    """
    test _Calibrator class
    :return:
    """
    calibrator = _Mapper(100, 50)
    detected_box = [25, 50, 75, 100]
    expected_box = [50, 100, 150, 200]
    calibrated_box = calibrator(detected_box)

    assert expected_box == calibrated_box
