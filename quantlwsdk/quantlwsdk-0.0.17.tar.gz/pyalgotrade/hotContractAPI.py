

#本模块只要是李文用来处理主力连续换月的一些动作


"""
.. moduleauthor:: lw
"""

from pyalgotrade import commonHelpBylw

class hotContractObj(object):

    """A group of :class:`Bar` objects.

    :param barDict: A map of instrument to :class:`Bar` objects.
    :type barDict: map.

    .. note::
        All bars must have the same datetime.
    """

    def __init__(self, mainContractData,calendarObj):
        self.__mainContractData = mainContractData
        self.calendarObj=calendarObj


    def getCurrHotSymbol(self,mainContract,date_):
        aHotSymbol=self.__mainContractData.loc[date_, mainContract]
        return aHotSymbol



    def getHotContractLastTDays(self,symbol,currTDays,mainContinueContract=None):
        # 获取上一个交易日的主力合约 代码

        #mainContinueContract是指给定主力连续的代码，比如SHFE.RB,一般不给，就是用具体的合约symbol
        #比如是SHFE.rb1910


        if not self.__mainContractData is None:

            # 获取上一个交易日


            lastTradeDates = self.calendarObj.tradingDaysOffset(currTDays, -1)
            # 上一个交易日存在
            if not lastTradeDates is None:


                if not mainContinueContract:
                    mainContinueContract = commonHelpBylw.getMainContinContract(symbol)

                lastSymbol = self.__mainContractData.loc[lastTradeDates, mainContinueContract]
                return lastSymbol


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
        # 获取当前日主力合约 代码

        if self.__mainContractData.index.contains(currTDays):
            mainContract = commonHelpBylw.getMainContinContract(symbol)
            currMainSymbol = self.__mainContractData.loc[currTDays, mainContract]
        else:
            currMainSymbol=None
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



    def isHotLastTDays(self,symbol,currTDays):
        # 判断该品种本交易日的上一个交易日是不是主力合约

        flag=False
        lasthotSymbol=self.getHotContractLastTDays(symbol,currTDays)

        if lasthotSymbol==symbol:
            flag=True

        return flag


    def isHotLastTDatetimes(self,symbol,aDatetime):
        # 判断该品种本交易日的上一个交易日是不是主力合约,但是是给定了datetime的，
        #即是在盘中考虑，而且是夜盘之分的。

        lastTradingDay = self.calendarObj.tradeDateTimeTradingDateOffset(aDatetime, -1)
        lasthotSymbol = self.getHotContractCurrDays(symbol, lastTradingDay)

        flag=False


        if lasthotSymbol==symbol:
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


    def isNeedMovePositionNDays(self,symbol,currTDays):
        # 判断该品种下个交易日是不是应该移仓了

        #本来isHotChangeTDays 也是干这个事情的，但是实际情况是，假如1号是rb1805，2号主力是rb1810
        # 其实1号如果rb1805发出了信号，那么还是在2号的1805上 交易，因为你在1号结束的时候，你不知道
        #能知道明天的主力合约是哪个合约的
        #只有到了2号结束，你发现rb1805 2号不是主力，但是rb1805 1号是主力，那么在2号，对rb1805而言
        #就要移仓了。

        #即规则是：如果当前symbol 今日收盘后不是主力，昨日收盘后是主力，所以要移仓

        flag=False

        lastHotSymbol =self.getHotContractLastTDays(symbol,currTDays)
        currHotSymbol= self.getHotContractCurrDays(symbol,currTDays)
        if currHotSymbol!=lastHotSymbol  and symbol==lastHotSymbol:
            flag=True


        return flag
