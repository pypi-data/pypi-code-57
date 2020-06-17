# -*- coding: utf-8 -*-
"""
test module for audio spectrum analysis
"""

from pathlib import Path

import numpy as np
import pandas as pd
from pytest import fixture

from sail_utils.audio.spectrum import FreqAnalysis


@fixture(name="freq_analysis")
def _freq_analysis_fixture():
    file_path = Path(__file__).absolute().parents[1] / "data/1586915489.wav"
    return FreqAnalysis(file_path.as_posix())


def test_freq_analysis_freq_features(freq_analysis):
    """
    test freq_features in FreqAnalysis
    :param freq_analysis:
    :return:
    """
    buckets = [[0, 50],
               [500, 800],
               [950, 1050],
               [1450, 1550],
               [1950, 2050],
               [2450, 2550],
               [3450, 3550]]
    start_offset = 5
    window = 5
    cutoff = 5000
    calculated = freq_analysis.freq_feature(buckets,
                                            start_offset=start_offset,
                                            window=window,
                                            cutoff=cutoff)

    freq, spec = freq_analysis.spectrum(start_offset=start_offset,
                                        window=window,
                                        cutoff=cutoff)
    freq_series = pd.Series(data=np.abs(spec), index=freq)

    expected = []
    for bucket in buckets:
        width = bucket[1] - bucket[0]
        selected_freq = freq_series[bucket[0]:bucket[1]]
        expected.append(np.sum(selected_freq) / width)

    expected = np.array(expected)
    np.testing.assert_array_almost_equal(calculated, expected)
