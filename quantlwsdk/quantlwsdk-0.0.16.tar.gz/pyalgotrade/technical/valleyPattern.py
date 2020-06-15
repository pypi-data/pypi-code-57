# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

from pyalgotrade import dataseries

from pyalgotrade.technical import lw_crossSeries
from pyalgotrade.technical import ma

#生产黄金谷，死亡谷序列
#
class GoldValley(dataseries.SequenceDataSeries):
    """
    """

    def __init__(self, shortSeries, middleSeries, longSeries,maxLen=None):
        super(GoldValley, self).__init__(maxLen)
        # self.__shortSeries=shortSeries
        # self.__middleSeries=middleSeries
        # self.__longSeries = longSeries

        longSeries.getNewValueEvent().subscribe(self.__onNewValue)

        self.__shortMiddCross=lw_crossSeries.crossSignals(shortSeries,middleSeries)
        self.__shortLongCross = lw_crossSeries.crossSignals(shortSeries, longSeries)
        self.__middLongCross = lw_crossSeries.crossSignals(middleSeries, longSeries)

        self.shortMiddGoldCrossFlag=False
        self.shortLongGoldCrossFlag = False
        self.middleLongGoldCrossFlag = False




    def __onNewValue(self):




        #测算黄金谷 第一个角
        if len(self.__shortMiddCross) >= 1:

            if self.__shortMiddCross[-1] is None:
                return
        else:
            return

        if self.__shortMiddCross[-1]==1:
            self.shortMiddGoldCrossFlag=True
        if self.__shortMiddCross[-1]==-1:
            self.shortMiddGoldCrossFlag = False

        # 测算黄金谷 第2个角
        if len(self.__shortLongCross) >= 1:

            if self.__shortLongCross[-1] is None:
                return
        else:
            return

        if self.__shortLongCross[-1]==1:
            self.shortLongGoldCrossFlag=True
        if self.__shortLongCross[-1]==-1:
            self.shortLongGoldCrossFlag = False

        # 测算黄金谷 第3个角 。同时也是判断黄金谷
        if len(self.__middLongCross) >= 2:

            if self.__middLongCross[-2] is None:
                return
        else:
            return
        #
        # if self.__middLongCross[-1] == 1:
        #     self.middleLongGoldCrossFlag = True
        # if self.__middLongCross[-1] == -1:
        #     self.middleLongGoldCrossFlag = False

        dtFromDs3 = self.__middLongCross.getDateTimes()[-1]
        if self.shortMiddGoldCrossFlag and self.shortLongGoldCrossFlag and \
                (self.__middLongCross[-1]==1 and self.__middLongCross[-2]!=1):

            self.appendWithDateTime(dtFromDs3, 1)
        else:
            self.appendWithDateTime(dtFromDs3,-88)







class valleySignal(dataseries.SequenceDataSeries):
    """
    """

    def __init__(self, dataSeries,shortPeriod, middlePeriod, longPeriod,maxLen=None):
        super(valleySignal, self).__init__(maxLen)

        maxLen = 20

        self.__maShort = ma.SMA(dataSeries, period=shortPeriod, maxLen=maxLen)
        self.__maMid = ma.SMA(dataSeries, period=middlePeriod, maxLen=maxLen)
        self.__maLong = ma.SMA(dataSeries, period=longPeriod, maxLen=maxLen)


        self.__shortMiddCross=lw_crossSeries.crossSignals(self.__maShort,self.__maMid,maxLen=maxLen)
        self.__shortLongCross = lw_crossSeries.crossSignals(self.__maShort, self.__maLong,maxLen=maxLen)
        self.__middLongCross = lw_crossSeries.crossSignals(self.__maMid, self.__maLong,maxLen=maxLen)

        dataSeries.getNewValueEvent().subscribe(self.__onNewValue)


        #1是黄金谷，-1是死亡谷，0 都不是
        self.shortMiddGoldCrossFlag=0
        self.shortLongGoldCrossFlag = 0
        self.middleLongGoldCrossFlag = 0




    def __onNewValue(self, dataSeries, dateTime, value):




        #测算黄金谷 第一个角
        if len(self.__shortMiddCross) >= 1:

            if self.__shortMiddCross[-1] is None:
                return
        else:
            return

        if self.__shortMiddCross[-1]==1:
            self.shortMiddGoldCrossFlag=1
        if self.__shortMiddCross[-1]==-1:
            self.shortMiddGoldCrossFlag = -1
        # if self.__shortMiddCross[-1]==0:
        #     self.shortMiddGoldCrossFlag = 0

        # 测算黄金谷 第2个角
        if len(self.__shortLongCross) >= 1:

            if self.__shortLongCross[-1] is None:
                return
        else:
            return

        if self.__shortLongCross[-1] == 1:
            self.shortLongGoldCrossFlag = 1
        if self.__shortLongCross[-1] == -1:
            self.shortLongGoldCrossFlag = -1
        # if self.__shortLongCross[-1] == 0:
        #     self.shortLongGoldCrossFlag = 0

        # 测算黄金谷 第3个角 。同时也是判断黄金谷
        if len(self.__middLongCross) >= 2:

            if self.__middLongCross[-2] is None:
                return
        else:
            return
        #
        # if self.__middLongCross[-1] == 1:
        #     self.middleLongGoldCrossFlag = True
        # if self.__middLongCross[-1] == -1:
        #     self.middleLongGoldCrossFlag = False

        sigvalue=0

        dtFromDs3 = self.__middLongCross.getDateTimes()[-1]
        if self.shortMiddGoldCrossFlag==1 and self.shortLongGoldCrossFlag==1 and \
                (self.__middLongCross[-1]==1 and self.__middLongCross[-2]!=1):

            sigvalue=1
        if self.shortMiddGoldCrossFlag == -1 and self.shortLongGoldCrossFlag == -1 and \
                (self.__middLongCross[-1] == -1 and self.__middLongCross[-2] != -1):
            sigvalue = -1

        self.appendWithDateTime(dtFromDs3, sigvalue)


