# -*- coding:utf-8 -*-

"""
获取基金净值数据接口
Created on 2020/6/15
@author: Meng Lv
@group: Howbuy FDC
@contact: meng.lv@howbuy.com
"""

from __future__ import division
import time
import json
import re
import pandas as pd
import numpy as np
from hbshare.fund import cons as ct
import hbshare as hbs

def get_fund_newest_nav_by_code(code, retry_count=3, pause=0.01, timeout=10):
    """
        获得公募基金最新净值（含最新回报，区间回报）
    :param code:
    :return:
    """
    api = hbs.hb_api()
    for _ in range(retry_count):
        time.sleep(pause)
        ct._write_console()
        url = ct.HOWBUY_FUND_NEWEST_NAV %(ct.P_TYPE['https'], ct.DOMAINS['hbcgi'],code)

        # request = Request(ct.HOWBUY_FUND_NEWEST_NAV %
        #                   (ct.P_TYPE['https'], ct.DOMAINS['hbcgi'],
        #                    code))
        # text = urlopen(request, timeout=timeout).read()
        # text = text.decode('gbk')

        org_js = api.query(url)
        status_code = int(org_js['common']['responseCode'])
        if status_code != 1:
            status = str(org_js['common']['responseContent'])
            raise ValueError(status)

        if 'opens' not in org_js:
            status = "未查询到该基金数据"
            raise ValueError(status)

        data = org_js['opens']
        fund_df = pd.DataFrame(data, columns=ct.HOWBUY_FUND_NEWEST_NAV_COLUMNS)
        fund_df['jjjz'] = fund_df['jjjz'].astype(float)
        fund_df['ljjz'] = fund_df['ljjz'].astype(float)
        fund_df['hbdr'] = fund_df['hbdr'].astype(float)
        fund_df['hb1y'] = fund_df['hb1y'].astype(float)
        fund_df['hb3y'] = fund_df['hb3y'].astype(float)
        fund_df['hb6y'] = fund_df['hb6y'].astype(float)
        fund_df['hbjn'] = fund_df['hbjn'].astype(float)
        fund_df['hb1n'] = fund_df['hb1n'].astype(float)
        fund_df['zfxz'] = fund_df['zfxz'].astype(float)
        return fund_df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)
