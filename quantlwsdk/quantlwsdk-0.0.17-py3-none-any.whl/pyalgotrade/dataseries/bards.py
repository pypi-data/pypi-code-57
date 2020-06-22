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

import six


class BarDataSeries(dataseries.SequenceDataSeries):
    """A DataSeries of :class:`pyalgotrade.bar.Bar` instances.

    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, maxLen=None):
        super(BarDataSeries, self).__init__(maxLen)
        self.__openDS = dataseries.SequenceDataSeries(maxLen)
        self.__closeDS = dataseries.SequenceDataSeries(maxLen)
        self.__highDS = dataseries.SequenceDataSeries(maxLen)
        self.__lowDS = dataseries.SequenceDataSeries(maxLen)
        self.__volumeDS = dataseries.SequenceDataSeries(maxLen)
        self.__adjCloseDS = dataseries.SequenceDataSeries(maxLen)
        self.__extraDS = {}
        self.__useAdjustedValues = False

    def __getOrCreateExtraDS(self, name):
        ret = self.__extraDS.get(name)
        if ret is None:
            ret = dataseries.SequenceDataSeries(self.getMaxLen())
            self.__extraDS[name] = ret
        return ret

    def setUseAdjustedValues(self, useAdjusted):
        self.__useAdjustedValues = useAdjusted

    def append(self, bar):
        self.appendWithDateTime(bar.getDateTime(), bar)

    def appendWithDateTime(self, dateTime, bar):
        assert(dateTime is not None)
        assert(bar is not None)
        bar.setUseAdjustedValue(self.__useAdjustedValues)

        # super(BarDataSeries, self).appendWithDateTime(dateTime, bar)

        self.__openDS.appendWithDateTime(dateTime, bar.getOpen())
        self.__closeDS.appendWithDateTime(dateTime, bar.getClose())
        self.__highDS.appendWithDateTime(dateTime, bar.getHigh())
        self.__lowDS.appendWithDateTime(dateTime, bar.getLow())
        self.__volumeDS.appendWithDateTime(dateTime, bar.getVolume())
        self.__adjCloseDS.appendWithDateTime(dateTime, bar.getAdjClose())

        # Process extra columns.
        for name, value in six.iteritems(bar.getExtraColumns()):
            extraDS = self.__getOrCreateExtraDS(name)
            extraDS.appendWithDateTime(dateTime, value)


        #这是lw后来发现的bug，因为原始的bar 在append的时候，close 这种数据都没准备好。
        #如果bards 要去驱动某个罗i，要用到bar的序列数据，那么序列数据根本没准备好。所以这句话从上面哪下来
        super(BarDataSeries, self).appendWithDateTime(dateTime, bar)

    def getOpenDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the open prices."""
        return self.__openDS

    def getCloseDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the close prices."""
        return self.__closeDS

    def getHighDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the high prices."""
        return self.__highDS

    def getLowDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the low prices."""
        return self.__lowDS

    def getVolumeDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the volume."""
        return self.__volumeDS

    def getAdjCloseDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the adjusted close prices."""
        return self.__adjCloseDS

    def getPriceDataSeries(self):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` with the close or adjusted close prices."""
        if self.__useAdjustedValues:
            return self.__adjCloseDS
        else:
            return self.__closeDS

    def getExtraDataSeries(self, name):
        """Returns a :class:`pyalgotrade.dataseries.DataSeries` for an extra column."""
        return self.__getOrCreateExtraDS(name)

        # #这个地方lw 李文提供的说明
        #这个地方会创建extrad的列，appen中也会如此。我遇到过个bug，增加数据的时候用的是‘position’列
        #但是getExtraDataSeries的时候，名字用错了，用了futurePosition,导致出现了2列。

        #本来像修正，但是似乎无从修复，因为上面这2中逻辑似乎都有道理。一种是新增数据，那么要多一列，一种是如果没有新增数据，
        #主动获取一列在前面，那么也合理

        #有一种需求是 新增数据在 主动获取一列之后。比如跨周期中，日线的feed是要传入到策略中，但是日线的数据还没新增，而是分钟数据在增加
        #此时就是主动获取一列（在策略初始化中出现）会在新增数据之前



        #另外一种需求是，新增数据在主动获取一列之前。比如 正常单周期中。策略初始化在在新增数据之前，这个和上面一样
        #但是如果初始化中，有些列，你没有主动取获取，而是留在了onbar中取获取，那么此时 该列就不会生成了，而新增数据的时候
        #就拿不到这列。 这种情况也会出现的。

        #所以上面的方案，只能是小心用了，即获取额外的列的时候，新增数据的列的时候，列名字要小心了。




