#!/usr/bin/python
#coding:utf-8

"""
@author: Meng.lv
@contact: meng.lv@howbuy.com
@software: PyCharm
@file: fund_nav_test.py
@time: 2020/6/15 10:50
"""

import hbshare as hbs


def test_get_fund_newest_nav():
    hbs.set_token("qwertyuisdfghjkxcvbn1000")
    data = hbs.get_fund_newest_nav_by_code('000004')
    print data


if __name__ == "__main__":
    test_get_fund_newest_nav()