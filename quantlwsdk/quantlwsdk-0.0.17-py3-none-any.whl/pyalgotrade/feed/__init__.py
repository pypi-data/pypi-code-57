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

import abc

from pyalgotrade import observer
from pyalgotrade import dataseries
from pyalgotrade import hotContractAPI
#import pandas as pd
from pyalgotrade.bar import Frequency
from pyalgotrade.bar import BasicBar

from pyalgotrade.utils import freMapFromGM
def feed_iterator(feed):
    feed.start()
    try:
        while not feed.eof():
            yield feed.getNextValuesAndUpdateDS()
    finally:
        feed.stop()
        feed.join()


class BaseFeed(observer.Subject):
    """Base class for feeds.

    :param maxLen: The maximum number of values that each :class:`pyalgotrade.dataseries.DataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded
        from the opposite end.
    :type maxLen: int.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, maxLen):
        super(BaseFeed, self).__init__()

        maxLen = dataseries.get_checked_max_len(maxLen)

        self.__ds = {}
        self.__event = observer.Event()
        self.__maxLen = maxLen







    def reset(self):
        keys = list(self.__ds.keys())
        self.__ds = {}
        for key in keys:
            self.registerDataSeries(key)

    # Subclasses should implement this and return the appropriate dataseries for the given key.
    @abc.abstractmethod
    def createDataSeries(self, key, maxLen):
        raise NotImplementedError()

    # Subclasses should implement this and return a tuple with two elements:
    # 1: datetime.datetime.
    # 2: dictionary or dict-like object.
    @abc.abstractmethod
    def getNextValues(self):
        raise NotImplementedError()

    def registerDataSeries(self, key):
        if key not in self.__ds:
            self.__ds[key] = self.createDataSeries(key, self.__maxLen)

    #lw在这加了一个注销某个品种的序列的操作。
    def unRegisterDataSeries(self, key):
        if key  in self.__ds:
            del self.__ds[key]
            # self.__ds[key] = self.createDataSeries(key, self.__maxLen)




    def getNextValuesAndUpdateDS(self):
        dateTime, values = self.getNextValues()
        if dateTime is not None:
            for key, value in values.items():
                # Get or create the datseries for each key.
                try:
                    ds = self.__ds[key]
                except KeyError:
                    ds = self.createDataSeries(key, self.__maxLen)
                    self.__ds[key] = ds
                ds.appendWithDateTime(dateTime, value)
        return (dateTime, values)

    def __iter__(self):
        return feed_iterator(self)

    def getNewValuesEvent(self):
        """Returns the event that will be emitted when new values are available.
        To subscribe you need to pass in a callable object that receives two parameters:

         1. A :class:`datetime.datetime` instance.
         2. The new value.
        """
        return self.__event

    def dispatch(self):
        dateTime, values = self.getNextValuesAndUpdateDS()
        if dateTime is not None:
            self.__event.emit(dateTime, values)
        return dateTime is not None

    def getKeys(self):
        return list(self.__ds.keys())
    
    
    
    # dfData 列名是 品种symbol,index 为时间，内容为具体的值，即可以是收盘价，开盘价等。
    #作者lw
    def updateDSFromDF(self,dfData,keepNan=True):

        symbols=list(dfData.columns.values)
        
        for aDT,aValue in dfData.iterrows():
            dateTime=aDT
            
#            print(dateTime)
            for aSymbol in symbols:
                
                if aSymbol=='SHFE.bu1806' and dateTime=='2017-12-29':
                    i=1
                value=aValue[aSymbol]

                if keepNan:
                    try:
                        ds = self.__ds[aSymbol]
                    except KeyError:
                        ds = self.createDataSeries(aSymbol, self.__maxLen)
                        self.__ds[aSymbol] = ds
                    ds.appendWithDateTime(dateTime, value)
                else:#如果强调，品种的行情没有，那么这个日期虽然是交易日，但是不收录。
                    if not np.isNan(value):
                        try:
                            ds = self.__ds[aSymbol]
                        except KeyError:
                            ds = self.createDataSeries(aSymbol, self.__maxLen)
                            self.__ds[aSymbol] = ds
                        ds.appendWithDateTime(dateTime, value)
  
    
    # updateOneDS 第一个symbol，第二个datetime，第三个value
    #作者lw
    def updateOneDS(self,data):  
        
        aSymbol=data[0]
        value=data[2]
        dateTime=data[1]
        try:
            ds = self.__ds[aSymbol]
        except KeyError:
            ds = self.createDataSeries(aSymbol, self.__maxLen)
            self.__ds[aSymbol] = ds
        ds.appendWithDateTime(dateTime, value)
        # if dateTime is not None:
        #     # self.__event.emit(dateTime, data)
        #     self.__event.emit(data)


    def __getitem__(self, key):
        """Returns the :class:`pyalgotrade.dataseries.DataSeries` for a given key."""
        return self.__ds[key]

    def __contains__(self, key):
        """Returns True if a :class:`pyalgotrade.dataseries.DataSeries` for the given key is available."""
        return key in self.__ds


    #这玩意儿是lw设计的，为了让feed带一个交易日序列。设计成属性。设置可读可写

    @property
    def calendarObj(self):
        return self.__canlendarObj

    @calendarObj.setter
    def calendarObj(self,aCalendar):
        self.__canlendarObj = aCalendar


    # #lw李文添加
    # def setMainConinueObj(self,mainContractData):
    #     self.hotContractObj=hotContractAPI.hotContractObj(mainContractData)



# class BaseOuterFeed(observer.Subject):
class BaseOuterFeed():
    """Base class for outerfeeds.
    这玩意是李文lw写的。目的在 pyalgotrade的改进笔记中有记载。
    :param maxLen: The maximum number of values that each :class:`pyalgotrade.dataseries.DataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded
        from the opposite end.
    :type maxLen: int.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, calendarObj,maxLen):
        # super(BaseFeed, self).__init__()

        maxLen = dataseries.get_checked_max_len(maxLen)

        self.__ds = {}
        self.__event = observer.Event()
        self.__maxLen = maxLen


        #lw添加
        self.__canlendarObj=calendarObj

    def reset(self):
        keys = list(self.__ds.keys())
        self.__ds = {}
        for key in keys:
            self.registerDataSeries(key)

    # Subclasses should implement this and return the appropriate dataseries for the given key.
    @abc.abstractmethod
    def createDataSeries(self, key, maxLen):
        raise NotImplementedError()



    def registerDataSeries(self, key):
        if key not in self.__ds:
            self.__ds[key] = self.createDataSeries(key, self.__maxLen)

    # lw在这加了一个注销某个品种的序列的操作。
    def unRegisterDataSeries(self, key):
        if key in self.__ds:
            del self.__ds[key]
            # self.__ds[key] = self.createDataSeries(key, self.__maxLen)

    def updateDS(self,key_,dateTime,value):


        try:
            ds = self.__ds[key_]
        except KeyError:
            ds = self.createDataSeries(key_, self.__maxLen)
            self.__ds[key_] = ds
        ds.appendWithDateTime(dateTime, value)

    def __iter__(self):
        return feed_iterator(self)

    def getNewValuesEvent(self):
        """Returns the event that will be emitted when new values are available.
        To subscribe you need to pass in a callable object that receives two parameters:

         1. A :class:`datetime.datetime` instance.
         2. The new value.
        """
        return self.__event

    # def dispatch(self):
    #     dateTime, values = self.getNextValuesAndUpdateDS()
    #     if dateTime is not None:
    #         self.__event.emit(dateTime, values)
    #     return dateTime is not None

    def getKeys(self):
        return list(self.__ds.keys())

    #  dfData 列名是 品种symbol,index 为时间，内容为具体的值，即可以是收盘价，开盘价等。
    # 作者lw
    def updateDSFromDF(self, dfData):

        for aDT, bar in dfData.iterrows():

            close_ = bar['close']
            open_ = bar['open']
            high_ = bar['high']
            low_ = bar['low']
            volume_ = bar['volume']
            gmfrestr = bar['frequency']
            pyalgoFre=freMapFromGM(gmfrestr)

            aSymbol=bar['symbol']



            

            adjClose = None
            ##这个if语句这么处理，真是无奈，因为掘金自己的数据问题
            if volume_ != 0:
                if high_ == 0:
                    high_ = close_
                if low_ == 0:
                    low_ = close_
                if open_ == 0:
                    open_ = close_



            try:
                abar = BasicBar(
                    aDT, open_, high_, low_, close_, volume_, adjClose, pyalgoFre
                )
            except Exception as e:
                print(e)
                return

            key_ = aSymbol + '-' + gmfrestr

            ds = self.__ds[key_]
            ds.appendWithDateTime(aDT, abar)



    


    def __getitem__(self, key):
        """Returns the :class:`pyalgotrade.dataseries.DataSeries` for a given key."""
        return self.__ds[key]

    def __contains__(self, key):
        """Returns True if a :class:`pyalgotrade.dataseries.DataSeries` for the given key is available."""
        return key in self.__ds

    # 这玩意儿是lw设计的，为了让feed带一个交易日序列。设计成属性。设置可读可写

    @property
    def calendarObj(self):
        return self.__canlendarObj

    @calendarObj.setter
    def calendarObj(self, aCalendar):
        self.__canlendarObj = aCalendar

