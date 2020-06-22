import datetime


class TimeRangeQuoteQuery(object):
    """
    行情请求参数
    """

    def __init__(self):
        self.startTime: datetime.datetime = None
        self.finishTime: datetime.datetime = None
        self.quoteCycleType = None
        self.contractCode = None
        self.exchange = None

    def __str__(self):
        return str.format(
            f"合约代码：{self.contractCode} 开始时间：{self.startTime} 结束时间：{self.finishTime} 周期：{self.quoteCycleType}")
