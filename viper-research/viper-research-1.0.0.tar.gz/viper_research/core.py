import pandas as pd
import requests

from viper_research.entity import TimeRangeQuoteQuery


class ViperResearch(object):
    """
    数据服务
    """
    RESTFUL_URL = "http://www.shyouxia.cn:8018"
    GET_TRADING_DAY_URL = RESTFUL_URL + "/get/trading/day"
    GET_FUTURE_SETTLEMENT_URL = RESTFUL_URL + "/get/future/settlement"
    GET_FUTURE_CATEGORY_URL = RESTFUL_URL + "/get/future/category"
    GET_FUTURE_CONTRACT_URL = RESTFUL_URL + "/get/future/contract"
    GET_STOCK_CONTRACT_URL = RESTFUL_URL + "/get/stock/contract"
    GET_CONTINUOUS_CONTRACT_URL = RESTFUL_URL + "/get/continuous/contract"
    GET_CONTINUOUS_ITEM_URL = RESTFUL_URL + "/get/continuous/item"
    GET_INDEX_CONTRACT_URL = RESTFUL_URL + "/get/index/contract"
    GET_INDEX_ITEM_URL = RESTFUL_URL + "/get/index/item"
    GET_BAR_QUOTE_URL = RESTFUL_URL + "/get/bar/quote"
    GET_TICK_QUOTE_URL = RESTFUL_URL + "/get/tick/quote"

    license_id = ""

    @staticmethod
    def set_license_id(license_id):
        """
        许可证编号
        :param license_id:许可证编号
        :return:None
        """
        ViperResearch.license_id = license_id

    @staticmethod
    def get_bar_quote(query: TimeRangeQuoteQuery):
        """
        获取K线行情
        :param query:查询参数
        :return:dataframe
        """
        params = dict()
        params['startTime'] = query.startTime.isoformat()
        params['finishTime'] = query.finishTime.isoformat()
        params['quoteCycleType'] = query.quoteCycleType
        params['contractCode'] = query.contractCode
        params['licenseId'] = ViperResearch.license_id
        params['exchange'] = query.exchange

        data = requests.get(url=ViperResearch.GET_BAR_QUOTE_URL, params=params)
        lines = data.text.split("\n")

        fields = lines[0].split(",")
        row_list = list()
        for line in lines[1:]:
            row_data = line.split(",")
            if len(row_data) == 7:
                row_list.append(row_data)

        pd_data = pd.DataFrame(row_list, columns=fields)
        if len(fields) < 7:
            return pd_data

        pd_data['high'] = pd.to_numeric(pd_data['high'], errors='coerce')
        pd_data['open'] = pd.to_numeric(pd_data['open'], errors='coerce')
        pd_data['low'] = pd.to_numeric(pd_data['low'], errors='coerce')
        pd_data['close'] = pd.to_numeric(pd_data['close'], errors='coerce')
        pd_data['volume'] = pd.to_numeric(pd_data['volume'], errors='coerce')

        return pd_data

    @staticmethod
    def get_tick_quote(query: TimeRangeQuoteQuery):
        """
        查询tick行情
        :param query:查询参数
        :return:dataframe
        """
        params = dict()
        params['startTime'] = query.startTime.isoformat()
        params['finishTime'] = query.finishTime.isoformat()
        params['quoteCycleType'] = query.quoteCycleType
        params['licenseId'] = ViperResearch.license_id
        params['contractCode'] = query.contractCode
        params['exchange'] = query.exchange

        data = requests.get(url=ViperResearch.GET_TICK_QUOTE_URL, params=params)
        lines = data.text.split("\n")

        fields = lines[0].split(",")
        columns = len(fields)
        row_list = list()
        for line in lines[1:]:
            row_data = line.split(",")
            if len(row_data) == columns:
                row_list.append(row_data)

        pd_data = pd.DataFrame(row_list, columns=fields)
        if columns <= 30:
            return pd_data

        pd_data['open'] = pd_data['open'].astype(float)
        pd_data['last'] = pd_data['last'].astype(float)
        pd_data['high'] = pd_data['high'].astype(float)
        pd_data['low'] = pd_data['low'].astype(float)

        pd_data['prev_close'] = pd_data['prev_close'].astype(float)
        pd_data['volume'] = pd_data['volume'].astype(float)

        pd_data['total_turnover'] = pd_data['total_turnover'].astype(float)
        pd_data['limit_up'] = pd_data['limit_up'].astype(float)
        pd_data['limit_down'] = pd_data['limit_down'].astype(float)

        pd_data['a1'] = pd_data['a1'].astype(float)
        pd_data['a2'] = pd_data['a2'].astype(float)
        pd_data['a3'] = pd_data['a3'].astype(float)
        pd_data['a4'] = pd_data['a4'].astype(float)
        pd_data['a5'] = pd_data['a5'].astype(float)

        pd_data['b1'] = pd_data['b1'].astype(float)
        pd_data['b2'] = pd_data['b2'].astype(float)
        pd_data['b3'] = pd_data['b3'].astype(float)
        pd_data['b4'] = pd_data['b4'].astype(float)
        pd_data['b5'] = pd_data['b5'].astype(float)

        pd_data['a1_v'] = pd_data['a1_v'].astype(float)
        pd_data['a2_v'] = pd_data['a2_v'].astype(float)
        pd_data['a3_v'] = pd_data['a3_v'].astype(float)
        pd_data['a4_v'] = pd_data['a4_v'].astype(float)
        pd_data['a5_v'] = pd_data['a5_v'].astype(float)

        pd_data['b1_v'] = pd_data['b1_v'].astype(float)
        pd_data['b2_v'] = pd_data['b2_v'].astype(float)
        pd_data['b3_v'] = pd_data['b3_v'].astype(float)
        pd_data['b4_v'] = pd_data['b4_v'].astype(float)
        pd_data['b4_v'] = pd_data['b4_v'].astype(float)

        pd_data['change_rate'] = pd_data['change_rate'].astype(float)

        if columns == 35:
            pd_data['prev_settlement'] = pd_data['prev_settlement'].astype(float)
            pd_data['open_interest'] = pd_data['open_interest'].astype(float)

        return pd_data
