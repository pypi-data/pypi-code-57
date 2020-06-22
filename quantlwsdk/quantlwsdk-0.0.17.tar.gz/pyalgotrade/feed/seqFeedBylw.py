# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:19:16 2018

@author: SH
"""






from pyalgotrade import dataseries
from pyalgotrade import feed
from pyalgotrade import commonHelpBylw



# This is only for backward compatibility since Frequency used to be defined here and not in bar.py.



class serialFeed(feed.BaseOuterFeed):
    
    def __init__(self, frequency, maxLen=None):
        super(serialFeed, self).__init__(maxLen)
        self.__frequency = frequency
        self.__currDatetime = None
        self.__currValue = None
        

        
    # def registerInstruments(self, instruments):
    #     for instrument in instruments:
    #         self.registerDataSeries(instrument)

# 

    def createDataSeries(self, key, maxLen):
        
        # ret = dataseries.SequenceDataSeries(maxLen,key)
        ret = dataseries.SequenceDataSeries(maxLen)
        return ret
    
    def setACurrValue(self,datetime_,value):
        self.__currDatetime=datetime_
        self.__currValue=value
        
    

    def stop(self):
        pass
    def start(self):
        pass
    def join(self):
        pass
    def getNextValues(self):
        
        return self.__currDatetime,self.__currValue
    def peekDateTime(self):
        pass
    def eof(self):
        pass
    
 
class serialMainContractsFeed(serialFeed):
    """
    这个类用来处理 主力连续的 一系列数据

    """

    def __init__(self, mainContractData,frequency,maxLen=None):
        # 这个如果不为none，则认为下单都要下到主力合约上，所以每次下单前，要检查，是否下个交易日，本合约仍为主力合约。
        super(serialMainContractsFeed, self).__init__(frequency, maxLen)
        self.__mainContractData = mainContractData



    def getCurrHotSymbol(self,mainContract,date_):
        aHotSymbol=self.__mainContractData.loc[date_, mainContract]
        return aHotSymbol

    def getHotContractNextTDays(self,symbol,currTDays):
        # 获取下一个主力合约 代码


        if not self.__mainContractData is None:

            # 获取下一个交易日
            nextTradeDates = self.calendarObj.tradingDaysOffset(currTDays, 1)
            # 下一个交易日存在
            if not nextTradeDates is None:
                mainContract = commonHelpBylw.getMainContinContract(symbol)
                nextSymbol = self.__mainContractData.loc[nextTradeDates, mainContract]
                return nextSymbol

    def getHotContractCurrDays(self,symbol,currTDays):
        # 获取下一个主力合约 代码
        mainContract = commonHelpBylw.getMainContinContract(symbol)
        currMainSymbol = self.__mainContractData.loc[currTDays, mainContract]
        return currMainSymbol






    def isHotNextTDays(self,symbol,currTDays):
        # 判断该品种下一个交易日是不是主力合约

        flag=False
        nextSymbol=self.getHotContractNextTDays(symbol, currTDays)
        if nextSymbol==symbol:
            flag=True


        return flag


    def isHotTDays(self,symbol,currTDays):
        # 判断该品种本交易日是不是主力合约

        flag=False
        currSymbol=self.getHotContractCurrDays(symbol, currTDays)
        if currSymbol==symbol:
            flag=True


        return flag



    def isHotChangeTDays(self,symbol,currTDays):
        # 判断该品种的主力连续是不是下一个交易日切换了

        flag=False
        # if not self.__mainContractData is None:
        #
        #     # 获取下一个交易日
        #     nextTradeDates = self.calendarObj.tradingDaysOffset(currTDays, 1)
        #     # 下一个交易日存在
        #     if not nextTradeDates is None:
        #         mainContract = commonHelpBylw.getMainContinContract(symbol)
        #         nextSymbol = self.__mainContractData.loc[nextTradeDates, mainContract]
        #         currMainSymbol=self.__mainContractData.loc[currTDays, mainContract]
        #         if currMainSymbol == symbol and nextSymbol != symbol:
        #             flag=True

        nexHotSymbol =self.getHotContractNextTDays(symbol,currTDays)
        currHotSymbol= self.getHotContractCurrDays(symbol,currTDays)
        if currHotSymbol!=nexHotSymbol  and symbol==currHotSymbol:
            flag=True


        return flag



