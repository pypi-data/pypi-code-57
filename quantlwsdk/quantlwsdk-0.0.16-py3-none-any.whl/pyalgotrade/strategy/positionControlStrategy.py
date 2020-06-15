
"""
20190822 09：45

lw 李文写的仓位控制模块
"""


from pyalgotrade.broker import gmEnum
from pyalgotrade import commonHelpBylw
import datetime

class intraDayPositionControl():
    def __init__(self, symbol,**kwargs):
        self.symbol = symbol
        # self.feed=feed

        # self.barDs=self.feed[self.symbol]

        self.intraOpenCountLimit=kwargs.get('intraOpenCountLimit', None)
        self.intraOpenLongCountLimit = kwargs.get('intraOpenLongCountLimit', None)
        self.intraOpenShortCountLimit = kwargs.get('intraOpenShortCountLimit', None)


        self.__intradaycLongOpenCount=0
        self.__intradaycShortOpenCount=0
        self.__intradayOpenCount=0

    def onbar(self,lastBarDT,currBarDT):
        # if len(self.barDs)>=2:
        # currDT = self.barDs.getDateTimes()[-1]
        # lastDT = self.barDs.getDateTimes()[-2]

        if commonHelpBylw.isCrossDay(self.symbol, lastBarDT, currBarDT):  # 跨日了，有些状态要重置。不能影响到下一日。
            self.__intradaycLongOpenCount = 0
            self.__intradaycShortOpenCount = 0
            self.__intradayOpenCount = 0

        longOpenLimitFlag = self.__intradaycLongOpenCount < self.intraOpenLongCountLimit
        shortOpenLimitFlag = self.__intradaycShortOpenCount < self.intraOpenShortCountLimit

        return longOpenLimitFlag,shortOpenLimitFlag




    #仓位控制，成交回报 就是会影响仓位。所以要有一个函数来应对这个事情。
    def onTradeReport(self,execrpt):
        # 多头开仓的回报
        if execrpt['position_effect'] == gmEnum.PositionEffect_Open and \
                execrpt['side'] == gmEnum.OrderSide_Buy:
            self.__intradaycLongOpenCount = self.__intradaycLongOpenCount + 1
            self.__intradayOpenCount=self.__intradayOpenCount+1
        # 多头开仓的回报
        if execrpt['position_effect'] == gmEnum.PositionEffect_Open and \
                execrpt['side'] == gmEnum.OrderSide_Sell:
            self.__intradaycShortOpenCount = self.__intradaycShortOpenCount + 1
            self.__intradayOpenCount=self.__intradayOpenCount+1

        i=1