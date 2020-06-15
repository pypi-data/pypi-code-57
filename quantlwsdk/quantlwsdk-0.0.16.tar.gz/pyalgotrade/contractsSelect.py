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
.. moduleauthor:: lw
"""

from gm.api import *

import  datetime
from pyalgotrade import commonHelpBylw
from pyalgotrade import gm3HelpBylw

class BaseStrategy4gmHot:
    """lw李文实现的，用来封装策略中的换月动作的，基于掘金的下单函数的.

    :param barFeed: The bar feed to use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BaseBarFeed`.
    :param cash_or_brk: The starting capital or a broker instance.
    :type cash_or_brk: int/float or :class:`pyalgotrade.broker.Broker`.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, symbol, feed, context):
        self.symbol = symbol
        self.context = context
        self.feed = feed
        # The broker should subscribe to barFeed events before the strategy.
        # This is to avoid executing orders submitted in the current tick.

    def hotChangeAction(self, aSymbol, cBarSDateTime):

        clearShortOrderRes = None
        openLongOrderRes = None
        clearLongOrderRes = None
        openShortOrderRes = None
            # 先查持仓
        symbolHolding = self.context.account().positions(symbol=aSymbol)
        if symbolHolding:

            if self.feed.hotContractObj.isNeedMovePositionNDays(aSymbol, cBarSDateTime):
            # if self.feed.hotContractObj.isHotChangeTDays(aSymbol, cBarSDateTime):
                nextHotSymbol = self.feed.hotContractObj.getHotContractNextTDays(aSymbol, cBarSDateTime)

                for aPos in symbolHolding:

                    vol_ = aPos['volume']
                    side_ = aPos['side']

                    if side_ == PositionSide_Long:
                            # 平仓
                        clearLongOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Sell,
                                         order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)

                            # 开仓
                        openLongOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Buy,
                                         order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

                    if side_ == PositionSide_Short:
                            # 平仓
                        clearShortOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Buy,
                                         order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)

                            # 开仓
                        openShortOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Sell,
                                         order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

        return openLongOrderRes,openShortOrderRes,clearLongOrderRes,clearShortOrderRes




#主力连续移仓
#asymbol是上一个主力合约，如果其有持仓，那么要平仓，同时仓位要在当前的主力合约上建立起来
def move_mainsymbol_position1(aSymbol,context,moveOrderLog=None):

    #注意，本函数并没有取判断asymbol是否已经到了主力换月的时候。所以需要外层来判断。


    clearShortOrderRes = None
    openLongOrderRes = None
    clearLongOrderRes = None
    openShortOrderRes = None
        # 先查持仓
    symbolHolding = context.account().positions(symbol=aSymbol)
    if symbolHolding:

        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        cdt=datetime.datetime.now()
        sDT=cdt - datetime.timedelta(days=1000)

        currDTstr = cdt.strftime('%Y-%m-%d %H:%M:%S')
        sDTstr=sDT.strftime('%Y-%m-%d %H:%M:%S')

        mainContractData = gm3HelpBylw.getMainContractData_Fade([mainContract], sDTstr, currDTstr)

        mainSymbolDf=mainContractData.stack().reset_index()
        mainSymbolDf.rename(index=str, columns={0: "symbol"}, inplace=True)

        lastDf=mainSymbolDf.loc[mainSymbolDf['symbol']==aSymbol].tail(1)
        lastDt=lastDf['datetime'].iloc[0]
        nextSymbolDf=mainSymbolDf.loc[mainSymbolDf['datetime']>lastDt].head(1)
        next_symbol=nextSymbolDf['symbol'].iloc[0]




        for aPos in symbolHolding:

            vol_ = aPos['volume']
            side_ = aPos['side']

            if side_ == PositionSide_Long:
                    # 平仓
                # clearLongOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Sell,
                #                  order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)


                if moveOrderLog is  not None:

                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_,'卖平')

                        # 开仓
                    moveOrderLog.info("%s,%s,%s", next_symbol, vol_, '买开')
                    # openLongOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Buy,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

                else:
                    # 存内存。
                    context.clearOrders_whenOpen[aSymbol]=(aSymbol, vol_,'卖平')
                    context.openOrders_whenOpen[next_symbol]=( next_symbol, vol_, '买开')


            if side_ == PositionSide_Short:

                if moveOrderLog is not None:
                    # 平仓
                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '买平')
                    # clearShortOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Buy,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)

                        # 开仓
                    moveOrderLog.info("%s,%s,%s", next_symbol, vol_, '卖开')
                    # openShortOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Sell,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)
                else:
                    # 存内存。


                    context.clearOrders_whenOpen[aSymbol] = (aSymbol, vol_, '买平')
                    context.openOrders_whenOpen[next_symbol] = (next_symbol, vol_, '卖开')
    # return openLongOrderRes,openShortOrderRes,clearLongOrderRes,clearShortOrderRes






#主力连续移仓

def move_mainsymbol_position(positions,latestTradeDate,context,moveOrderLog=None):

    #latestTradeDate 表示最近已经完成的交易日。比如20191107 11：00，那么此时20191107交易日没有完成，已经完成的最近的是20191106
    #moveOrderLog  这玩意 本来是为了将所有的移仓的动作都写文本，然后等待开盘时间到了后，从文本读取品种直接下单。但是后来发现
    #总不是从内存写到本地，然后到时候又要从本地读到内存，那我干脆直接存到内存算了

   
        # 先查持仓
    if len(positions)<=0:
        return
    underlyingAssets=[]
    for aposition in positions:
        aSymbol=aposition.symbol
        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        underlyingAssets.append(mainContract)
    # underlyingAssets=list(set(underlyingAssets))
    mainContractData = gm3HelpBylw.getMainContractData_Fade(underlyingAssets, latestTradeDate,latestTradeDate)



    # cdt=datetime.datetime.now()
    # sDT=cdt - datetime.timedelta(days=1000)
    #
    # currDTstr = cdt.strftime('%Y-%m-%d %H:%M:%S')
    # sDTstr=sDT.strftime('%Y-%m-%d %H:%M:%S')
    #
    # mainContractData = gm3HelpBylw.getMainContractData_Fade([mainContract], sDTstr, currDTstr)
    #
    # mainSymbolDf=mainContractData.stack().reset_index()
    # mainSymbolDf.rename(index=str, columns={0: "symbol"}, inplace=True)
    #
    #
    # # last2Df=mainSymbolDf.loc[mainSymbolDf['symbol']<aSymbol].tail(1)
    # # last2Dt=lastDf['datetime'].iloc[0]
    # # lastlastDf=mainSymbolDf.loc[mainSymbolDf['datetime']==last2Dt]
    # # last_symbol=lastlastDf['symbol'].iloc[0]
    #
    # Df = mainSymbolDf.loc[mainSymbolDf['datetime'] <= latestTradeDate].tail(2)
    # lastMainSymbol=Df['symbol'].iloc[0]
    # currSymbol = Df['symbol'].iloc[1]

    for aposition in positions:
        aSymbol=aposition.symbol
        mainContract = commonHelpBylw.getMainContinContract(aSymbol)
        currSymbol=mainContractData[mainContract].iloc[0]
        if aSymbol!=currSymbol:



            vol_ = aposition['volume']
            side_ = aposition['side']

            if side_ == PositionSide_Long:
                    # 平仓
                # clearLongOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Sell,
                #                  order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)


                if moveOrderLog is  not None:

                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_,'卖平')

                        # 开仓
                    moveOrderLog.info("%s,%s,%s", currSymbol, vol_, '买开')
                    # openLongOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Buy,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

                else:
                    # 存内存。
                    context.clearOrders_whenOpen[aSymbol]=(aSymbol, vol_,'卖平')
                    context.openOrders_whenOpen[currSymbol]=(currSymbol, vol_, '买开')


            if side_ == PositionSide_Short:

                if moveOrderLog is not None:
                    # 平仓
                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '买平')
                    # clearShortOrderRes=order_volume(symbol=aSymbol, volume=vol_, side=OrderSide_Buy,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)

                        # 开仓
                    moveOrderLog.info("%s,%s,%s", currSymbol, vol_, '卖开')
                    # openShortOrderRes=order_volume(symbol=nextHotSymbol, volume=vol_, side=OrderSide_Sell,
                    #                  order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)
                else:
                    # 存内存。


                    context.clearOrders_whenOpen[aSymbol] = (aSymbol, vol_, '买平')
                    context.openOrders_whenOpen[currSymbol] = (currSymbol, vol_, '卖开')
            # return openLongOrderRes,openShortOrderRes,clearLongOrderRes,clearShortOrderRes



#掘金主力指定的合约

def main_symbol_juejin_rule(dateTimeStr,aNewTradeCalendar,underLyingSymList):
    # 这个是当前时间，最近的已经完成了的交易日
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)
    mainContractData = gm3HelpBylw.getMainContractData_Fade(underLyingSymList, lastDate, lastDate)

    tt = list(mainContractData.values[0])

    return tt


def fisrt_two_Contracts_max_volume(dateTimeStr,aNewTradeCalendar,underlySym):


    # 这个是当前时间，最近的已经完成了的交易日
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)

    contractsdf = gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym, nextTradeDate, nextTradeDate)

    symbolist=list(contractsdf['symbol'].values)
    sDt=lastDate+' 00:00:00'
    edt=lastDate+' 23:59:59'
    volDf=gm3HelpBylw.getHQData_Fade(symbolist,sDt,edt,fre='1d',fields_='symbol,eob,volume')

    # 1、下一个交易日需要 满足王总那个表要求的那些合约

    volDf['underLyingSym'] = volDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    volDf = volDf.groupby('underLyingSym').apply(lambda x: x.sort_values('volume',ascending=False))
    volDf= volDf.reset_index( drop=True)
    volDf = volDf.groupby('underLyingSym').head(2)

    contract1List = list(volDf['symbol'].values)

    # 2、将不符合要求的合约也列出来
    leftContractsList=list(set(symbolist).difference(set(contract1List)))

    return contract1List,leftContractsList


#王总定义的合约前一个月1号就撤走逻辑
def last_month_of_Contracts_delisted_date(dateTimeStr,aNewTradeCalendar,underlySym):

    #这个是当前时间，最近的已经完成了的交易日
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)

    contractsdf=gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym,nextTradeDate,nextTradeDate)



    from pandas.tseries.offsets import  MonthBegin
    import pandas as pd
    contractsdf['lastMonthDate']=pd.to_datetime(contractsdf['delisted_date'])+MonthBegin(-2)
    contractsdf['lastMonthDate'] = contractsdf['lastMonthDate'].dt.strftime('%Y-%m-%d')






    #1、下一个交易日需要 满足王总那个表要求的那些合约
    newContracDf = contractsdf.loc[nextTradeDate < contractsdf['lastMonthDate']]
    newContracDf['underLyingSym'] = newContracDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    newContracDf = newContracDf.groupby('underLyingSym').apply(lambda x: x.sort_values('delisted_date'))
    newContracDf.index = newContracDf.index.droplevel(0)
    newContracDf = newContracDf.groupby('underLyingSym').head(2)

    contract1List=list(newContracDf['symbol'].values)

    # 2、下一个交易日按照 王总那个表 需要剔除的那些合约，但是呢，这些合约有持仓了。所以这些合约也需要保留下来

    keepContracDf = contractsdf.loc[nextTradeDate >= contractsdf['lastMonthDate']]
    leftContractsList=list(keepContracDf['symbol'].values)
    return contract1List, leftContractsList

#王总定义的第二中合约切换逻辑，所有合约均在0414，0814，1214 这3个日期经受检查。
def special_date_of_Contracts_delisted_date(dateTimeStr,aNewTradeCalendar,underLyingSymList):



    #这个是当前时间，最近的已经完成了的交易日
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)

    import pandas as pd
    pDf = pd.read_excel('策略合约.xlsx', header=0)
    pDf['日期']=pDf['日期'].dt.strftime('%Y-%m-%d')
    aContractRow = pDf.loc[pDf['日期']<=nextTradeDate].iloc[-1]
    aContractRow = aContractRow.reset_index(drop=True)
    aContractRow = aContractRow.dropna()

    adjustContract = aContractRow.iloc[1:]

    #测试要回测的品种是否在这个表中提供了参数，没有的话要报出来异常。
    for aunderLysym in underLyingSymList:
        if aunderLysym not in adjustContract.values:
            ex = Exception()
            raise ex

    boolflag = adjustContract.apply(gm3HelpBylw.isUnderlyingSymbl)
    adjustContract = adjustContract[~boolflag]
    adjustContract = adjustContract.apply(commonHelpBylw.adjustSymbol)




    #1、下一个交易日需要 满足王总那个表要求的那些合约
    contract1List=[]
    for asymbol in list(adjustContract.values):
        underLysym=commonHelpBylw.getMainContinContract(asymbol)
        if underLysym in underLyingSymList:
            contract1List.append(asymbol)
        i=1


    # contract1List=list(adjustContract.values)


    return contract1List
def special_date_of_Contracts_delisted_date_copy(dateTimeStr,aNewTradeCalendar,underlySym):

    #这个是当前时间，最近的已经完成了的交易日
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)

    contractsdf=gm3HelpBylw.getContractsByUnderlyingSymbols(underlySym,nextTradeDate,nextTradeDate)



    from pandas.tseries.offsets import  MonthBegin
    import pandas as pd



    dateIndex=pd.date_range('2019-01-01','2020-12-31')
    datedf=dateIndex.to_frame(index=False,name='date')
    datedf['date']=datedf['date'].dt.strftime('%Y-%m-%d')

    adjustDate=datedf.loc[datedf['date'].str[5:].isin(['04-15', '08-15', '12-15'])]



    comparedatedf=adjustDate.loc[adjustDate['date']<=nextTradeDate]
    comparedate=comparedatedf['date'].iloc[-1]

    #1、下一个交易日需要 满足王总那个表要求的那些合约
    newContracDf=contractsdf.copy()
    newContracDf['underLyingSym'] = newContracDf['symbol'].apply(commonHelpBylw.getMainContinContract)
    newContracDf = newContracDf.groupby('underLyingSym').apply(lambda x: x.sort_values('delisted_date'))
    newContracDf.index = newContracDf.index.droplevel(0)

    newContracDf=newContracDf.loc[(newContracDf['listed_date']<=comparedate)&(newContracDf['delisted_date']>=comparedate)]

    # contractGroupby=newContracDf.groupby('underLyingSym')
    newContracDf = newContracDf.groupby('underLyingSym').tail(2)

    contract1List=list(newContracDf['symbol'].values)

    # 2、下一个交易日按照 王总那个表 需要剔除的那些合约，但是呢，这些合约有持仓了。所以这些合约也需要保留下来

    keepContracDf = contractsdf.loc[nextTradeDate >= contractsdf['lastMonthDate']]
    leftContractsList=list(keepContracDf['symbol'].values)
    return contract1List, leftContractsList

#比如给定具体的品种，要取到当月合约
def mothContractByN(dateTimeStr,aNewTradeCalendar,underlySym,N):


    #取出当前上市合约。
    lastDate = aNewTradeCalendar.get_latest_finished_tradingdate(dateTimeStr)
    nextTradeDate = aNewTradeCalendar.tradingDaysOffset(lastDate, 1)

    contractsdf = gm3HelpBylw.getAllCanTradeContractsByUnderlyingSymbols(underlySym, nextTradeDate, nextTradeDate)

    contract1List=list(contractsdf['symbol'].values)
    for asymbol in contract1List:
        sec_id=asymbol.split('.')[1]
        monthID=sec_id[-2:]
        if monthID==dateTimeStr[5:7]:
            return asymbol
