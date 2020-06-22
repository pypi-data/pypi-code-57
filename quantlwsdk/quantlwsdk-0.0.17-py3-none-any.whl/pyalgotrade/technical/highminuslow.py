
"""
李文设计的 求 high减去low的绝对值序列
"""

from pyalgotrade import technical
from pyalgotrade.dataseries import bards
#lw加的
from pyalgotrade import commonHelpBylw

#这个函数是lw李文补得。用来提供 简单平均的方式 计算atr
class HighMiusLowEventWindow(technical.EventWindow):
    def __init__(self, period, useAdjustedValues):

        super(HighMiusLowEventWindow, self).__init__(period)
        self.__useAdjustedValues = useAdjustedValues

        self.__value = None

    def _calculateRange(self, value):


        tr1 = value.getClose(self.__useAdjustedValues) - value.getOpen(self.__useAdjustedValues)
        tr2 = abs(tr1)

        return tr2

    def onNewValue(self, dateTime, value):
        tr = self._calculateRange(value)
        super(HighMiusLowEventWindow, self).onNewValue(dateTime, tr)


        if value is not None and self.windowFull():

            self.__value = commonHelpBylw.round_up(self.getValues().mean(),2) #简单平均



    def getValue(self):
        return self.__value





class ATR(technical.EventBasedFilter):
    """
    """

    # def __init__(self, barDataSeries, period, useAdjustedValues=False, maxLen=None):
    #     if not isinstance(barDataSeries, bards.BarDataSeries):
    #         raise Exception("barDataSeries must be a dataseries.bards.BarDataSeries instance")
    #
    #     super(ATR, self).__init__(barDataSeries, ATREventWindow(period, useAdjustedValues), maxLen)
    #

     #lw 要修改代码，将原始代码注释在上面。

    def __init__(self, barDataSeries, useAdjustedValues=False, maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception("barDataSeries must be a dataseries.bards.BarDataSeries instance")

        if type=='sma':
            awindow=ATRSmaEventWindow(period, useAdjustedValues)
        if type=='ema':
            awindow = ATREventWindow(period, useAdjustedValues)

        super(ATR, self).__init__(barDataSeries, awindow, maxLen)
