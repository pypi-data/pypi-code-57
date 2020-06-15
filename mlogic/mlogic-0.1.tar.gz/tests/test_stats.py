from mlogic.utils import stats
import numpy as np


def test_ttest():
    sample1 = np.random.randn(1000) + 0.2
    sample2 = np.random.randn(1000)
    p_value = stats.ttest(sample1, sample2)
    assert p_value < 0.05


def test_ftest():
    sampels = [np.random.randn(1000) + (x / 5) for x in range(1, 4)]
    p_value = stats.ftest(sampels)
    assert p_value < 0.05


def test_cross_value():
    s1 = list("acacacc")
    nrow = len(set(s1))
    s2 = list("kjjkkkj")
    ncol = len(set(s2))
    assert stats.cross_value(s1, s2).shape == (nrow, ncol)


def test_chi2_contingency():
    s1 = list("acacacacaccaac")
    s2 = list("jkjkjkjkjkjkjk")
    # print(stats.cross_value(s1, s2))
    p_value = stats.chi2_contingency(s1, s2)
    assert p_value < 0.05
