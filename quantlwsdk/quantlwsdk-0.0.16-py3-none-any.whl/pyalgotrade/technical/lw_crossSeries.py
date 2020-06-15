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

#主要是用来生产金叉死叉序列
#不一定是ma的金叉死叉，任意两个时间序列的金叉死叉。


class crossSignals(dataseries.SequenceDataSeries):
    """
    这个地方，为什么入参要是2个序列，因为这里是要判断任意两个序列的交叉。如果在
    类里面来生产序列，你不知道未来 是什么序列进来。一般可能是close的 ma 两个序列来判断交叉

    但是有时候，可能需要判断2个ema序列交叉。那在类里面写死就不好。
    """

    def __init__(self, dataSeries1, dataSeries2, maxLen=None):
        super(crossSignals, self).__init__(maxLen)
        self.__ds1=dataSeries1
        self.__ds2=dataSeries2
        dataSeries2.getNewValueEvent().subscribe(self.__onNewValue)


    def __onNewValue(self, dataSeries, dateTime, value):

        #要计算当前时间的上穿还是下穿，至少得2个序列（包含当前序列在内）
        if len(self.__ds1)>=2 and len(self.__ds2)>=2:


            #首先检查时间
            dtFromDs1 = self.__ds1.getDateTimes()[-1]
            dtFromDs2 = self.__ds2.getDateTimes()[-1]
            assert (dtFromDs1 == dtFromDs2)

            sedtFromDs1 = self.__ds1.getDateTimes()[-2]
            sedtFromDs2 = self.__ds2.getDateTimes()[-2]
            assert (sedtFromDs1 == sedtFromDs2)

            newValue = 0
            #金叉

            if not self.__ds1[-2] is None and not self.__ds2[-2] is None:
                if self.__ds1[-2]<self.__ds2[-2] and self.__ds1[-1]>=self.__ds2[-1]:
                    newValue=1
                # 死叉
                if self.__ds1[-2] > self.__ds2[-2] and self.__ds1[-1] <= self.__ds2[-1]:
                    newValue = -1

                self.appendWithDateTime(dtFromDs1, newValue)

