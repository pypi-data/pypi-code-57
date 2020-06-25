#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import rqdatac as rq
import pickle as pkl
from typing import List
from .EMQuantAPI_Python.python3.EmQuantAPI import *
import datetime
import json
import os
import csv
import traceback
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker
from ...wrapper.mysql import RawDatabaseConnector
from ...view.raw_models import *
from ...api.basic import BasicDataApi
from ...api.raw import RawDataApi
from .raw_data_helper import RawDataHelper

class EmRawDataDownloader(object):

    def __init__(self, data_helper):
        self._data_helper = data_helper
        # ForceLogin
        # 取值0，当线上已存在该账户时，不强制登录
        # 取值1，当线上已存在该账户时，强制登录，将前一位在线用户踢下线
        options = 'ForceLogin=1'
        loginResult = c.start(options, mainCallBack=self._main_callback)
        if(loginResult.ErrorCode != 0):
            print('EM login failed')
            exit()

        self._scale_change_dates = ['0331', '0630', '0930', '1231']

    def _main_callback(self, quantdata):
        '''
        mainCallback 是主回调函数，可捕捉连接错误
        该函数只有一个为c.EmQuantData类型的参数quantdata
        :param quantdata: c.EmQuantData
        '''
        print(f'MainCallback: {quantdata}')

    def _get_date_list(self, start_date, end_date):
        start_datetime = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
        date_list = []
        while start_datetime <= end_datetime:
            date_list.append(start_datetime.strftime('%Y%m%d'))
            start_datetime += datetime.timedelta(days=1)
        return date_list

    def em_fund_nav_history(self, nav_file_dir):
        try:
            index = 1
            for filename in os.listdir(nav_file_dir):
                if filename.endswith(".xls"):
                    print(f'{index}: {filename}')
                    index += 1
                    fund_nav = pd.concat(pd.read_excel(os.path.join(nav_file_dir, filename), sheet_name=None),
                                        ignore_index=True)
                    fund_nav = fund_nav.drop(['简称'], axis=1)
                    fund_nav = fund_nav.rename(columns={
                        '代码': 'CODES',
                        '时间': 'DATES',
                        '单位净值(元)': 'ORIGINALUNIT',
                        '累计净值(元)': 'ORIGINALNAVACCUM',
                        '复权净值(元)': 'ADJUSTEDNAV',
                        '万份基金单位收益(元)': 'UNITYIELD10K',
                        '7日年化收益率(%)': 'YIELDOF7DAYS'
                    })

                    fund_nav = fund_nav[(fund_nav['DATES'] != '--')
                                        & (~fund_nav['DATES'].isnull())]
                    fund_nav = fund_nav.replace('--', np.nan)
                    self._data_helper._upload_raw(fund_nav, EmFundNav.__table__.name)
                else:
                    continue
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_index_price_history(self, em_ids, start_date, end_date):
        em_id_str = ','.join(em_ids) if em_ids is list else em_ids
        df = c.csd(em_id_str, "CLOSE", start_date, end_date,
                   "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

        df = df.reset_index().rename(columns={
            'CODES': 'em_id',
            'DATES': 'datetime',
            'CLOSE': 'close'
        })

        self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)

    def em_fund_scale_history(self):
        date_funds = {}
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                dates = db_session.query(
                    distinct(EmFundNav.DATES)
                ).all()

                dates = [d for d, in dates]
                dates.sort()
                start_date = dates[0]
                for i in range(1, 100):
                    dates.insert(0, start_date - datetime.timedelta(days=i))

                for d in dates:
                    month_day = d.strftime('%m%d')
                    if month_day not in self._scale_change_dates:
                        continue

                    print(d)

                    fund_ids = db_session.query(
                        distinct(EmFundNav.CODES)
                    ).filter(
                        EmFundNav.DATES >= d,
                        EmFundNav.DATES <= d + datetime.timedelta(days=100)
                    ).all()

                    fund_ids = [f for f, in fund_ids]
                    fund_id_str = ','.join(fund_ids)

                    df = c.css(fund_id_str, "FUNDSCALE",
                               f"EndDate={d},Ispandas=1").reset_index()
                    df['DATES'] = d

                    self._data_helper._upload_raw(df, EmFundScale.__table__.name)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def em_fund_holding_rate_history(self):
        # 机构持有比例半年更新，到期日未必有数据，会有延迟， 含已终止基金
        fund_id_result = c.sector('507010', '2020-06-10')
        fund_list = fund_id_result.Data[0::2]
        fund_id_str = ','.join(fund_list)
        y_list = [str(y) for y in range(2010, 2020,1)]
        d_list = []
        for y in y_list:
            for d in ['-06-30', '-12-31']:
                d_list.append(y+d)
        for d in d_list:
            data=c.css(fund_id_str,"HOLDPERSONALHOLDINGPCT,HOLDINSTIHOLDINGPCT",f"ReportDate={d} ,Ispandas=1")
            data['DATES'] = d
            data = data.reset_index().dropna()
            self._data_helper._upload_raw(data, EmFundHoldingRate.__table__.name)
            print(f'finish {d} ')

    def em_fund_nav(self, start_date, end_date):
        try:
            # Get all fund ids, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=5)
            start_date = start_date.strftime('%Y%m%d')
            self.delete_em_fund_nav(start_date, end_date)
            fund_id_result = c.sector('507013', end_date)
            if fund_id_result.ErrorCode != 0:
                print(f'Failed to get fund id list: {fund_id_result.ErrorMsg}')
                return

            fund_id_list = fund_id_result.Data[0::2]
            fund_id_str = ','.join(fund_id_list)

            df = c.csd(fund_id_str, 'ORIGINALUNIT,ORIGINALNAVACCUM,ADJUSTEDNAV,10KUNITYIELD,YIELDOF7DAYS',
                    start_date, end_date, 'AdjustFlag=2,Ispandas=1')

            # print(df)
            df.reset_index(inplace=True)
            df['UNITYIELD10K'] = df['10KUNITYIELD']
            df = df.drop(['10KUNITYIELD'], axis=1)
            self._data_helper._upload_raw(df, EmFundNav.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def delete_em_fund_nav(self, start_date, end_date):
        try:
            RawDataApi().delete_em_fund_nav(start_date, end_date)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False    

    def em_fund_scale(self, start_date, end_date):
        try:
            # Get all fund ids, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            fund_id_result = c.sector('507013', end_date)
            if fund_id_result.ErrorCode != 0:
                print(f'Failed to get fund id list: {fund_id_result.ErrorMsg}')
                return

            fund_id_list = fund_id_result.Data[0::2]
            fund_id_str = ','.join(fund_id_list)

            for d in self._get_date_list(start_date, end_date):
                df = c.css(fund_id_str, 'FUNDSCALE', f'EndDate={d},Ispandas=1').reset_index()
                df['DATES'] = d
                self._data_helper._upload_raw(df, EmFundScale.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_index_price(self, em_ids, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=5)
        start_date = start_date.strftime('%Y%m%d')
        self.delete_em_index_price(em_ids, start_date, end_date)
        try:
            res = []
            if isinstance(em_ids, list):
                for em_id in em_ids:
                    df = c.csd(em_id, "CLOSE", start_date, end_date, "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
                    res.append(df)
                df = pd.concat(res)
            else:
                df = c.csd(em_ids, "CLOSE", start_date, end_date, "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")

            df = df.reset_index().rename(columns={
                'CODES': 'em_id',
                'DATES': 'datetime',
                'CLOSE': 'close'
            })

            self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def delete_em_index_price(self, em_ids, start_date, end_date):
        try:
            RawDataApi().delete_em_index_price(em_ids, start_date, end_date)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False    

    def em_index(self, start_date, end_date):
        # ----------------------
        # H11073.CSI,信用债
        # SPX.GI,标普500
        # GDAXI.GI,德国DAX
        # N225.GI,日经225
        # 000012.SH,利率债
        # 000300.SH,沪深300
        # 000905.SH,中证500
        # 399006.SZ,创业板
        # 801181.SWI,房地产开发申万
        # ----------------------
        # USDCNY.IB,美元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # JPYCNY.IB,日元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # EURCNY.IB,欧元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # ----------------------
        # AU0.SHF,沪金主力连续,TODO: always get None
        # BC.ICE,布伦特原油当月连续,TODO: always get None
        # ----------------------
        codes = (
                 'H11073.CSI,SPX.GI,GDAXI.GI,N225.GI,000012.SH,000300.SH,000905.SH,399006.SZ,801181.SWI,'
                 'USDCNY.IB,JPYCNY.IB,EURCNY.IB,'
                #  'AU0.SHF,BC.ICE'
        )
        df = c.csd(codes, 'CLOSE', start_date, end_date, 'Ispandas=1')
        if df is not None:
            df.reset_index(inplace=True)
            print(df)
            # self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)

    # 从em客户端导出数据后读取并处理
    def em_stock_price_history(self, stock_price_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_price_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_price = pd.concat(pd.read_excel(os.path.join(stock_price_file_dir, filename), sheet_name=None, na_values='--'),
                                    ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_price = stock_price.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '开盘价(元)': 'OPEN',
                '收盘价(元)': 'CLOSE',
                '最高价(元)': 'HIGH',
                '最低价(元)': 'LOW',
                '前收盘价(元)': 'PRECLOSE',
                '均价(元)': 'AVERAGE',
                '成交量(股)': 'VOLUME',
                '成交金额(元)': 'AMOUNT',
                '换手率(%)': 'TURN',
                '交易状态': 'TRADESTATUS',
                '内盘成交量': 'BUYVOL',
                '外盘成交量': 'SELLVOL',
            })

            # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
            stock_price = stock_price.loc[stock_price['TRADESTATUS'] != '未上市'].loc[~stock_price['DATES'].isna()].rename(columns=lambda x: EmStockPrice.__getattribute__(EmStockPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(stock_price, EmStockPrice.__table__.name)

    def em_stock_price(self, start_date: str, end_date: str):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_price] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_price] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return

            df_list = []
            for date in tradedates.Data:
                # 获取个股股价信息
                temp_df = c.csd(stock_id_result.Codes,
                                'OPEN,CLOSE,HIGH,LOW,PRECLOSE,AVERAGE,VOLUME,AMOUNT,TURN,TRADESTATUS,TNUM,BUYVOL,SELLVOL',
                                date, date, 'period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock price info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
                df_list.append(temp_df.loc[temp_df['TRADESTATUS'] != '未上市'].loc[~temp_df['DATES'].isna()])

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockPrice.__getattribute__(EmStockPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    # 从em客户端导出数据后读取并处理
    def em_stock_post_price_history(self, stock_post_price_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_post_price_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_price = pd.concat(pd.read_excel(os.path.join(stock_post_price_file_dir, filename), sheet_name=None, na_values='--'),
                                    ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_price = stock_price.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '开盘价(元)': 'OPEN',
                '收盘价(元)': 'CLOSE',
                '最高价(元)': 'HIGH',
                '最低价(元)': 'LOW',
                '前收盘价(元)': 'PRECLOSE',
                '均价(元)': 'AVERAGE',
                '成交量(股)': 'VOLUME',
                '成交金额(元)': 'AMOUNT',
                '交易状态': 'TRADESTATUS',
            })
            # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
            stock_price = stock_price.loc[stock_price['TRADESTATUS'] != '未上市'].loc[~stock_price['DATES'].isna()].rename(columns=lambda x: EmStockPostPrice.__getattribute__(EmStockPostPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(stock_price, EmStockPostPrice.__table__.name)

    def em_stock_post_price(self, start_date: str, end_date: str):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_post_price] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_post_price] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return

            df_list = []
            for date in tradedates.Data:
                # 获取个股股价信息
                temp_df = c.csd(stock_id_result.Codes,
                                'OPEN,CLOSE,HIGH,LOW,PRECLOSE,AVERAGE,VOLUME,AMOUNT,TRADESTATUS,TAFACTOR',
                                date, date, 'period=1,adjustflag=2,curtype=1,order=1,market=0,Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock price info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
                df_list.append(temp_df.loc[temp_df['TRADESTATUS'] != '未上市'].loc[~temp_df['DATES'].isna()])

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockPostPrice.__getattribute__(EmStockPostPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockPostPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_stock_info(self, end_date: str):
        # 获取所有A股股票的ID, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        # 全部A股股票
        stock_id_result = c.sector('001004', end_date)
        if stock_id_result.ErrorCode != 0:
            print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
            return

        df_list: List[pd.DataFrame] = []
        # 获取无参数指标
        df_no_param = c.css(stock_id_result.Codes,
                            'NAME,LISTDATE,FINPURCHORNOT,FINSELLORNOT,STOHSTOCKCONNECTEDORNOT,SHENGUTONGTARGET,ENGNAME,COMPNAME,COMPNAMEENG',
                            'Ispandas=1')
        if not isinstance(df_no_param, pd.DataFrame) and df_no_param.ErrorCode != 0:
            print(f'failed to get stock info(no param): {df_no_param.ErrorMsg}')
        else:
            # 将其中'是'/'否'的结果转换为True/False
            columns = ['FINPURCHORNOT', 'FINSELLORNOT', 'STOHSTOCKCONNECTEDORNOT', 'SHENGUTONGTARGET']
            df_no_param.loc[:, columns] = df_no_param.loc[:, columns].apply(lambda x: x.apply(lambda x: True if x == '是' else False))
            df_list.append(df_no_param)

        # 获取行业分类共有三级的指标
        df_lv4 = c.css(stock_id_result.Codes, "BLEMINDCODE,BLSWSINDCODE,SW2014CODE,EMINDCODE2016,CITICCODE2020", "ClassiFication=4,Ispandas=1")
        if not isinstance(df_lv4, pd.DataFrame) and df_lv4.ErrorCode != 0:
            print(f'failed to get stock info(lv4): {df_lv4.ErrorMsg}')
        else:
            df_list.append(df_lv4)

        # 获取行业分类共有二级的指标
        df_lv3 = c.css(stock_id_result.Codes, "BLCSRCINDCODE,CSRCCODENEW", "ClassiFication=3,Ispandas=1")
        if not isinstance(df_lv3, pd.DataFrame) and df_lv3.ErrorCode != 0:
            print(f'failed to get stock info(lv3): {df_lv3.ErrorMsg}')
        else:
            df_list.append(df_lv3)

        # 获取行业分类共有四级的指标
        df_lv5 = c.css(stock_id_result.Codes, "CSINDCODE2016,GICSCODE", "ClassiFication=5,Ispandas=1")
        if not isinstance(df_lv5, pd.DataFrame) and df_lv5.ErrorCode != 0:
            print(f'failed to get stock info(lv5): {df_lv5.ErrorMsg}')
        else:
            df_list.append(df_lv5)

        if len(df_list) > 0:
            # 将每部分按列粘到一起
            df = pd.concat(df_list, axis=1)
            # 不需要存日期的列，去除索引并做列名转换
            df = df.drop(columns='DATES').reset_index().rename(columns=lambda x: EmStockInfo.__getattribute__(EmStockInfo, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockInfo.__table__.name)

    def add_columns_to_fin_fac(self, end_date: str):
        # 获取所有A股股票的ID, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        # 全部A股股票
        stock_id_result = c.sector('001004', end_date)
        if stock_id_result.ErrorCode != 0:
            print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
            return

        # 获取主营收入构成(按产品)
        df = c.css(stock_id_result.Codes, "BALANCESTATEMENT_195", f'ReportDate={end_date},type=1,Ispandas=1')
        if not isinstance(df, pd.DataFrame) and df.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df.ErrorMsg}')
            return

        count = 0
        Session = sessionmaker(RawDatabaseConnector().get_engine())
        db_session = Session()
        for row in db_session.query(EmStockFinFac):
            if row.DATES != datetime.datetime.strptime(end_date, '%Y%m%d').date():
                continue
            if row.CODES in df.index:
                row.BALANCESTATEMENT_195 = df.at[row.CODES, 'BALANCESTATEMENT_195']
                count += 1
        db_session.commit()
        db_session.close()
        print(f'append {count} value(s) to fin fac table')

    def em_stock_fin_fac(self, end_date: str):
        # 获取所有A股股票的ID, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        # 全部A股股票
        stock_id_result = c.sector('001004', end_date)
        if stock_id_result.ErrorCode != 0:
            print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
            return

        df_list: List[pd.DataFrame] = []
        # 获取无参数指标
        df_no_param = c.css(stock_id_result.Codes,
                            'EBIT,EBITDA,EXTRAORDINARY,LOWERDIANDNI,GROSSMARGIN,OPERATEINCOME,INVESTINCOME,EBITDRIVE,TOTALCAPITAL,WORKINGCAPITAL,\
                             NETWORKINGCAPITAL,TANGIBLEASSET,RETAINED,INTERESTLIBILITY,NETLIBILITY,EXINTERESTCL,EXINTERESTNCL,FCFF,FCFE,DA,FCFFDRIVE,\
                             PERFORMANCEEXPRESSPARENTNI,MBSALESCONS,GPMARGIN,NPMARGIN,EXPENSETOOR,INVTURNRATIO,ARTURNRATIO,ROEAVG,ROEWA,EPSBASIC,EPSDILUTED,\
                             BPS,BALANCESTATEMENT_25,BALANCESTATEMENT_46,BALANCESTATEMENT_93,BALANCESTATEMENT_103,BALANCESTATEMENT_141,BALANCESTATEMENT_195,\
                             BALANCESTATEMENT_140,INCOMESTATEMENT_9,INCOMESTATEMENT_48,INCOMESTATEMENT_60,INCOMESTATEMENT_61,INCOMESTATEMENT_85,INCOMESTATEMENT_127,\
                             INCOMESTATEMENT_14,CASHFLOWSTATEMENT_39,CASHFLOWSTATEMENT_59,CASHFLOWSTATEMENT_77,CASHFLOWSTATEMENT_82,CASHFLOWSTATEMENT_86',
                            f'ReportDate={end_date},type=1,Ispandas=1')
        if not isinstance(df_no_param, pd.DataFrame) and df_no_param.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_no_param.ErrorMsg}')
        else:
            df_list.append(df_no_param)

        # 获取主营收入构成(按产品)
        df_mb_sales_cons = c.css(stock_id_result.Codes, "MBSALESCONS", f'ReportDate={end_date},type=2,Ispandas=1')
        if not isinstance(df_mb_sales_cons, pd.DataFrame) and df_mb_sales_cons.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_mb_sales_cons.ErrorMsg}')
        else:
            df_list.append(df_mb_sales_cons.rename(columns={'MBSALESCONS': 'MBSALESCONS_P'}))

        # 获取归属于上市公司股东的扣除非经常性损益后的净利润(调整前)
        df_with_param_1 = c.css(stock_id_result.Codes, "DEDUCTEDINCOME", f'ReportDate={end_date},DataAdjustType=1,Ispandas=1')
        if not isinstance(df_with_param_1, pd.DataFrame) and df_with_param_1.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_with_param_1.ErrorMsg}')
        else:
            df_list.append(df_with_param_1.rename(columns={'DEDUCTEDINCOME': 'DEDUCTEDINCOME_BA'}))

        # 获取归属于上市公司股东的扣除非经常性损益后的净利润(调整后)
        df_with_param_2 = c.css(stock_id_result.Codes, "DEDUCTEDINCOME", f'ReportDate={end_date},DataAdjustType=2,Ispandas=1')
        if not isinstance(df_with_param_2, pd.DataFrame) and df_with_param_2.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_with_param_2.ErrorMsg}')
        else:
            df_list.append(df_with_param_2.rename(columns={'DEDUCTEDINCOME': 'DEDUCTEDINCOME_AA'}))

        # 获取TTM指标
        df_ttm = c.css(stock_id_result.Codes, 'GRTTMR,GCTTMR,ORTTMR,OCTTMR,EXPENSETTMR,GROSSMARGINTTMR,OPERATEEXPENSETTMR,ADMINEXPENSETTMR,FINAEXPENSETTMR,IMPAIRMENTTTMR,\
                       OPERATEINCOMETTMR,INVESTINCOMETTMR,OPTTMR,NONOPERATEPROFITTTMR,EBITTTMR,EBTTTMR,TAXTTMR,PNITTMR,KCFJCXSYJLRTTMR,\
                       NPTTMRP,FVVPALRP,IRTTMRP,IITTMFJVAJVRP,BTAATTMRP,SALESCASHINTTMR,CFOTTMR,CFITTMR,CFFTTMR,CFTTMR,CAPEXR',
                       f'ReportDate={end_date},Ispandas=1')
        if not isinstance(df_ttm, pd.DataFrame) and df_ttm.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_ttm.ErrorMsg}')
        else:
            df_list.append(df_ttm)

        if len(df_list) > 0:
            # 将每部分按列粘到一起
            df = pd.concat(df_list, axis=1)
            # 日期列修改为end_date
            df.loc[:, 'DATES'] = end_date
            df = df.reset_index().rename(columns=lambda x: EmStockFinFac.__getattribute__(EmStockFinFac, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockFinFac.__table__.name)

    # 从em客户端导出数据后读取并处理
    def em_stock_daily_info_history(self, stock_daily_info_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_daily_info_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_daily_info = pd.concat(pd.read_excel(os.path.join(stock_daily_info_file_dir, filename), sheet_name=None, na_values='--'),
                                         ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_daily_info = stock_daily_info.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '总股本(股)': 'TOTALSHARE',
            })

            stock_daily_info = stock_daily_info.loc[~stock_daily_info['DATES'].isna()].rename(columns=lambda x: EmStockDailyInfo.__getattribute__(EmStockDailyInfo, x).name)

            # 更新到db
            self._data_helper._upload_raw(stock_daily_info, EmStockDailyInfo.__table__.name)

    def em_stock_daily_info(self, start_date: str, end_date: str, predict_year: int = 0):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_daily_info] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_daily_info] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return

            if predict_year == 0:
                predict_year = datetime.datetime.strptime(end_date, '%Y%m%d').date().year

            df_list = []
            for date in tradedates.Data:
                temp_df = c.css(stock_id_result.Codes,
                                'TOTALSHARE,HOLDFROZENAMTACCUMRATIO,ASSETMRQ,EQUITYMRQ,PETTMDEDUCTED,PBLYRN,PSTTM,AHOLDER,ESTPEG',
                                f'EndDate={date},TradeDate={date},PREDICTYEAR={predict_year},Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock daily info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 日期列修改为end_date
                temp_df.loc[:, 'DATES'] = date
                df_list.append(temp_df)

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockDailyInfo.__getattribute__(EmStockDailyInfo, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockDailyInfo.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_stock_refinancing(self, start_date: str, end_date: str):
        try:
            data = c.ctr("AdditionPlanInfo",
                         "SECURITYCODE,APPROVENOTICEDATE,PLANNOTICEDDATE,NEWPROGRESS,SUMFINA_T,ATTACHNAME,ADDPURPOSE",
                        f"DateType=2,StartDate={start_date},EndDate={end_date},Process=0")
            if data.ErrorCode != 0:
                print(f'failed to get stock refinancing info: {data.ErrorMsg}')
                return False

            infos: List[List] = []
            for v in data.Data.values():
                # if v[3] in ('董事会批准', '董事会修改', '董事会终止', '股东大会批准', '股东大会修改'):
                #    continue
                infos.append(v)
            df = pd.DataFrame(infos, columns=['SECURITYCODE', 'APPROVENOTICEDATE', 'PLANNOTICEDDATE',
                                              'NEWPROGRESS', 'SUMFINA_T', 'ATTACHNAME', 'ADDPURPOSE'])
            self._data_helper._upload_raw(df.rename(columns=lambda x: EmStockRefinancing.__getattribute__(EmStockRefinancing, x).name), EmStockRefinancing.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_index_val(self, start_date: str, end_date: str):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_index_val] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_index_val] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            # 获取basic table中index_info信息
            index_info_df = BasicDataApi().get_index_info()
            # 下边几个指数特殊处理
            special_list = "399006.SZ,000300.SH,000905.SH,SPX.GI"
            # 获取index_info中满足条件的上述几个指数之外的所有指数
            other_indexes = index_info_df[~index_info_df.loc[:, 'em_id'].isin(special_list.split(',')) & index_info_df.loc[:, 'tag_method'].isin(['PE百分位', 'PB百分位'])]['em_id'].dropna()

            '''
            def transform_tradedates(x: str):
                day, month, year = x.split('/')
                return datetime.date(int(day), int(month), int(year)).strftime('%Y/%m/%d')
            transformed_tradedates = list(map(transform_tradedates, tradedates.Data))
            '''
            df_list = []
            for date in tradedates.Data:
                # 一天一天地获取
                indexes_df = c.csd(special_list,
                                "PETTM,PBMRQ,DIVIDENDYIELD,PSTTM,PCFTTM,ROE,EPSTTM",
                                date, date,
                                "DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1")
                if not isinstance(indexes_df, pd.DataFrame) and indexes_df.ErrorCode != 0:
                    print(f'failed to get index val info: {indexes_df.ErrorMsg} (date){date}')
                    return
                # df_list.append(indexes_df.loc[indexes_df['DATES'].isin(transformed_tradedates), :])
                df_list.append(indexes_df)

                # 两组指数可能获取的日期范围有一些区别，所以分开获取
                other_indexes_df = c.csd(other_indexes.to_list(),
                                        "PETTM,PBMRQ,DIVIDENDYIELD,PSTTM,PCFTTM,ROE,EPSTTM",
                                        date, date,
                                        "DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1")
                if not isinstance(other_indexes_df, pd.DataFrame) and other_indexes_df.ErrorCode != 0:
                    print(f'failed to get index val info: {other_indexes_df.ErrorMsg} (date){date}')
                    return
                # df_list.append(other_indexes_df.loc[other_indexes_df['DATES'].isin(transformed_tradedates), :])
                df_list.append(other_indexes_df)

            # 更新到db
            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmIndexVal.__getattribute__(EmIndexVal, x).name)
            self._data_helper._upload_raw(df, EmIndexVal.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_tradedates(self, start_date, end_date):
        try:
            tradedates_result = c.tradedates(start_date, end_date,"period=1,order=1,market=CNSESH")
            if tradedates_result.ErrorCode != 0:
                print(f'Failed to get tradedates: {tradedates_result.ErrorMsg}')
                return False

            tradedates = tradedates_result.Data
            df = pd.DataFrame(tradedates, columns=['TRADEDATES'])
            self._data_helper._upload_raw(df, EmTradeDates.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    def em_index_component(self, start_date: str, end_date: str):
        try:
            index_info = BasicDataApi().get_index_info()

            date_list = self._get_date_list(start_date, end_date)
            s_list: List[pd.Series] = []
            for row in index_info[~index_info['em_plate_id'].isna()].loc[:, ['index_id', 'em_id', 'em_plate_id']].itertuples(index=False):
                for date in date_list:
                    stock_id_result = c.sector(row.em_plate_id, date)
                    if stock_id_result.ErrorCode != 0:
                        # print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                        continue

                    stock_id_list: List[str] = []
                    for i in range(0, len(stock_id_result.Data), 2):
                        stock_id_list.append(stock_id_result.Data[i])
                    if len(stock_id_list) != 0:
                        s_list.append(pd.Series(row._asdict()).append(pd.Series({'datetime': date, 'stock_list': ','.join(stock_id_list)})))

            # 更新到db
            self._data_helper._upload_raw(pd.DataFrame(s_list), EmIndexComponent.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_stack()
            return

    def download_all(self, start_date, end_date):
        failed_tasks = []
        # If em_tradedates fails, there is no trading day between start_date and end_date
        # Stop and return
        if not self.em_tradedates(start_date, end_date):
            failed_tasks.append('em_tradedates')
            return failed_tasks

        if not self.em_fund_scale(start_date, end_date):
            failed_tasks.append('em_fund_scale')

        if not self.em_fund_nav(start_date, end_date):
            failed_tasks.append('em_fund_nav')

        if not self.em_index_price(['H00140.SH','H11025.CSI','AU0.SHF'], start_date, end_date):
            failed_tasks.append('em_index_price')

        if not self.em_stock_price(start_date, end_date):
            failed_tasks.append('em_stock_price')
        
        if not self.em_stock_post_price(start_date, end_date):
            failed_tasks.append('em_stock_post_price')

        if not self.em_index_val(start_date, end_date):
            failed_tasks.append('em_index_val')

        if not self.em_stock_daily_info(start_date, end_date):
            failed_tasks.append('em_stock_daily_info')

        if not self.em_index_component(start_date, end_date):
            failed_tasks.append('em_index_component')

        return failed_tasks


if __name__ == '__main__':
    data_helper = RawDataHelper()
    em = EmRawDataDownloader(data_helper)
    # em.em_index_val('20200428', '20200428')
    # em.em_fund_nav('20200415', '20200427')
    # em.em_index_price_history('H00140.SH', '20050101', '20200419')
    # em.em_fund_scale_history()
    # em.em_stock_fin_fac('20161231')
    # em.em_stock_info('20200424')
    # em.em_stock_price('20041231', '20041231')
    # em.em_stock_post_price('20041231', '20041231')
    # em.em_stock_daily_info('20041231', '20041231')
    # em.em_stock_price_history('./')
    # em.em_stock_post_price_history('./')
    # em.em_stock_daily_info_history('./')
    # em.em_stock_refinancing('20170101', '20181231')
    # em.add_columns_to_fin_fac('20190930')
    # em.em_fund_scale('20200513', '20200513')
    # em.em_index_component('20200528', '20200529')
