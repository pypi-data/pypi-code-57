

#李文lw 构造的kdj指标。

from pyalgotrade.technical import ma
from pyalgotrade.technical import highlow
from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards

from pyalgotrade import commonHelpBylw


class KDJ():
    """
    """

    def __init__(self, barDataSeries, N,M1,M2, useAdjustedValues=False,maxLen=None):
        if not isinstance(barDataSeries, bards.BarDataSeries):
            raise Exception("barDataSeries must be a dataseries.bards.BarDataSeries instance")
        assert (N > 0)
        assert (M1 > 0)

        assert (M2 > 0)
        # super(KDJ, self).__init__(dataSeries, KDJEventWindow(period), maxLen)
        self.__useAdjustedValues = useAdjustedValues
        self.__K = dataseries.SequenceDataSeries(maxLen)
        self.__D = ma.SMA(self.__K,M2,maxLen)
        self.__J = dataseries.SequenceDataSeries(maxLen)

        self.__rsvLLWindow = highlow.HighLowEventWindow(N,True)
        self.__rsvHHWindow = highlow.HighLowEventWindow(N, False)
        self.__KWindow = ma.SMAEventWindow(M1)
        barDataSeries.getNewValueEvent().subscribe(self.__onNewValue)

    def __onNewValue(self, dataSeries, dateTime, value):
        self.__rsvLLWindow.onNewValue(dateTime, value.getLow(self.__useAdjustedValues))
        self.__rsvHHWindow.onNewValue(dateTime, value.getHigh(self.__useAdjustedValues))

        if self.__rsvLLWindow.windowFull():

            currClose=value.getClose(self.__useAdjustedValues)
            currLL=self.__rsvLLWindow.getValue()
            currHH=self.__rsvHHWindow.getValue()
            rsv=commonHelpBylw.round_up((currClose-currLL)*100/(currHH-currLL),2)

            #计算k值
            self.__KWindow.onNewValue(dateTime, rsv)
            if self.__KWindow.windowFull():
                k=self.__KWindow.getValue()
                self.__K.appendWithDateTime(dateTime, k)

                #计算d值
                #d值在上面指标中自动计算了



                #计算j值
                if k is not None and (len(self.__D)>1 and self.__D[-1] is not None):
                    j=commonHelpBylw.round_up(3*k-2*self.__D[-1],2)
                    self.__J.appendWithDateTime(dateTime,j)


    def getK(self):

        return self.__K

    def getD(self):

        return self.__D

    def getJ(self):

        return self.__J







