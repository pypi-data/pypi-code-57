

"""
.. moduleauthor:: lw
用来处理独立出场逻辑
"""

from gm.api import *

from pyalgotrade import commonHelpBylw
from pyalgotrade import gm3HelpBylw
from pyalgotrade import dataseries
from pyalgotrade.utils import gmEnum
import copy
from pyalgotrade import loggerHelpbylw
import pandas as pd
# class BaseStopStrategy():
#     def __init__(self):
#
#         self.orderPostionList=[]
#
#     # 本函数，根据gm下单结果（开仓和平仓下单），来增加或者减少list中的orderPosition对象
#     #
#
#     def upDateorderPosiListByOpen(self,orderRe):
#         pass
#
#     def upDateorderPosiListByClear(self,orderRe):
#
#         position_effect = orderRe['position_effect']
#         positionSide = orderRe['position_side']
#         volNum_ = orderRe['filled_volume']
#         symbol_ = orderRe['symbol']
#         # 平仓
#         if position_effect == gmEnum.PositionEffect_Close:
#
#             for aOrderPosi in reversed(self.orderPostionList):
#                 if  (aOrderPosi.positionSide =='long' and positionSide==1) or\
#                 (aOrderPosi.positionSide =='short' and positionSide==2):
#                     if aOrderPosi.volume >= volNum_:
#                         aOrderPosi.volume = aOrderPosi.volume - volNum_
#                         break
#                     else:
#                         aOrderPosi.volume = 0
#                         volNum_ = volNum_ - aOrderPosi.volume
#             self.checkOrderPosiList()
#
#
#     def checkOrderPosiList(self):
#         # 清楚掉为0的持仓
#         templist = []
#         for aPosiMfe in self.orderPostionList:
#             if aPosiMfe.volume != 0:
#                 templist.append(aPosiMfe)
#
#         self.orderPostionList = copy.deepcopy(templist)
#         i = 1
#     def updateBarSinceEntry(self):
#         # 调整barsSinceEntry
#         for aOrderPosi in self.orderPostionList:
#             aOrderPosi.barsSinceEntry = aOrderPosi.barsSinceEntry + 1
#
#     def updateOrderPosition(self,orderRe):
#         if orderRe is None:
#             return
#         position_effect = orderRe['position_effect']
#         position_side = orderRe['position_side']
#         volNum_ = orderRe['filled_volume']
#         symbol_ = orderRe['symbol']
#
#         if position_side == gmEnum.PositionSide_Long:
#             positionSideStr = 'long'
#         if position_side == gmEnum.PositionSide_Short:
#             positionSideStr = 'short'
#
#         # 开仓
#         if position_effect == gmEnum.PositionEffect_Open:
#
#             cost_ = orderRe['filled_vwap']
#             commission_ = 0
#
#             aOrderPosition = BaseOrderHoldingPostion(symbol_, positionSideStr, volNum_, cost_,
#                                                      commission=commission_)
#             aOrderPosition.barsSinceEntry = -1  # 这里是因为 真正成交是下个bar成交的
#
#
#             self.orderPostionList.append(aOrderPosition)
#
#             # if symbol_ == strategyObj.symbol:
#             #     # self.orderPostionMfeList.append(adict)
#             #     strategyObj.orderPostionMfeList.append(adict)
#             # else:
#             #     # 访问其他合约的 策略对象
#             #     strategyObj.allSymStrategy[symbol_].orderPostionMfeList.append(adict)
#
#         # 平仓
#         if position_effect == gmEnum.PositionEffect_Close:
#
#             for aOrderPosi in reversed( self.orderPostionList):
#                 if aOrderPosi['orderPosition'].positionSide == positionSideStr:
#
#                     if aOrderPosi['orderPosition'].volume >= volNum_:
#                         aOrderPosi['orderPosition'].volume = aOrderPosi['orderPosition'].volume - volNum_
#                         break
#                     else:
#                         aOrderPosi['orderPosition'].volume = 0
#                         volNum_ = volNum_ - aOrderPosi['orderPosition'].volume







#
# class IndiviStop:
#
#
#     def __init__(self,orderPostionMfeList_):
#         self.orderPostionMfeList=orderPostionMfeList_
#
#         import logging
#         import sys
#         # 获取logger实例，如果参数为空则返回root logger
#
#         self.loggerCons = logging.getLogger("stopLossConsPrint")
#         # 指定logger输出格式
#         formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
#         # 控制台日志
#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.formatter = formatter  # 也可以直接给formatter赋值
#         # 为logger添加的日志处理器
#         if len(self.loggerCons.handlers)<1:
#             self.loggerCons.addHandler(console_handler)
#         # 指定日志的最低输出级别，默认为WARN级别
#         self.loggerCons.setLevel(logging.INFO)
#
#
#
#
#     def breakEvenStop(self,basicBar_,profitRate):
#         #profitRate 是指 收益率多少的时候，触发 breakeven 止损。
#
#
#         date_=basicBar_.getDateTime()
#
#
#         for aOrderPosiMFE in self.orderPostionMfeList:
#
#
#             # 2）计算mfe是否超过限额
#             aOrderPosi = aOrderPosiMFE['orderPosition']
#             symbol_= aOrderPosi.symbol
#             vol_= aOrderPosi.volume
#             cost_=aOrderPosi.cost
#             if symbol_=='CZCE.CF805' and date_[0:10]=='2018-01-12':
#                 i=1
#
#             if aOrderPosiMFE['MFE']:
#                 if aOrderPosiMFE['MFE'] > cost_ * (profitRate):
#                     aOrderPosiMFE['enableBreakEven']=True
#                 aOrderPosiMFE.setdefault('enableBreakEven', False)
#
#                 if aOrderPosiMFE['enableBreakEven']:
#                    if  aOrderPosi.positionSide=='long':
#                        if basicBar_.getLow()<=cost_:
#                            stopClearLongRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
#                                                order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)
#
#
#                             #更新orderPostionMfeList
#                            aOrderPosi.volume=0
#
#                            # if symbol_=='SHFE.cu1901':
#                            #      i=1
#                            # self.loggerCons.info("%s barDate:%s long position breakEven stop", symbol_, date_)
#
#                    if aOrderPosi.positionSide == 'short':
#                        if basicBar_.getHigh() >= cost_:
#                            stopclearShortRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
#                                                order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)
#
#                            # 更新orderPostionMfeList
#                            aOrderPosi.volume = 0
#
#                            # if symbol_=='CZCE.CF805':
#                            #      i=1
#                            # self.loggerCons.info("%s barDate:%s short position breakEven stop", symbol_, date_)
#
#
#
# class TrailingStopObj(BaseStopStrategy):
#
#     def __init__(self,atrDS):
#
#         super(TrailingStopObj,self).__init__()
#         self.__atrDS =  atrDS
#
#
#
#
#
# #这2个enable的意思是，因为有的跟踪止损策略，加了个限制，是要达到一定的条件
#     #才开启跟踪止损
#     def EnableTrailingWithProfit(self,profitRate):
#
#         for aOrderPosiMFE in self.orderPostionMfeList:
#             aOrderPosi = aOrderPosiMFE['orderPosition']
#             cost_ = aOrderPosi.cost
#             if aOrderPosiMFE['MFE'] > cost_ * (profitRate):
#                 aOrderPosiMFE['enableTrailing'] = True
#             aOrderPosiMFE.setdefault('enableTrailing', False)
#
#     def EnableTrailingWithATR(self,natr):
#
#         for aOrderPosi in self.orderPostionList:
#
#
#
#             if aOrderPosi.mfe:#这个是保证 mfe这个值有了，即但在委托后，到了下一个bar。并不是单子成交的那个bar
#
#                 cost_ = aOrderPosi.cost
#                 if aOrderPosi.positionSide == 'long':
#                     if aOrderPosi.mfe > self.__atrDS[-1]*natr:
#                         aOrderPosi.enableTrailing = True
#                 if aOrderPosi.positionSide == 'short':
#                     if aOrderPosi.mfe > self.__atrDS[-1]*natr:
#                         aOrderPosi.enableTrailing= True
#
#
#
#     def upDateorderPosiListByOpen(self,orderRe):
#         if orderRe is None:
#             return
#         position_effect = orderRe['position_effect']
#         position_side = orderRe['position_side']
#         volNum_ = orderRe['filled_volume']
#         symbol_ = orderRe['symbol']
#         createdTime_=orderRe['created_at'].strftime('%Y-%m-%d %H:%M:%S')
#
#         if position_side == gmEnum.PositionSide_Long:
#             positionSideStr = 'long'
#         if position_side == gmEnum.PositionSide_Short:
#             positionSideStr = 'short'
#
#         # 开仓
#         if position_effect == gmEnum.PositionEffect_Open:
#
#             cost_ = orderRe['filled_vwap']
#             commission_ = 0
#
#             aOrderPosition = BaseOrderHoldingPostion(symbol_, positionSideStr, volNum_, cost_,
#                                                      commission=commission_,createTime=createdTime_)
#             aOrderPosition.barsSinceEntry = -1  # 这里是因为 真正成交是下个bar成交的
#
#
#
#
#             #下面是 因为跟踪止损 是要跟踪mfe的，所以为实例动态增加一些字段
#             aOrderPosition.hh = None
#             aOrderPosition.ll = None
#             aOrderPosition.mfe = None
#             aOrderPosition.enableTrailing = False
#
#             self.orderPostionList.append(aOrderPosition)
#
#     def runStop(self, basicBar_,backNATR=1):
#         # profitRate 是指 收益率多少的时候，触发 trailingStop 止损。
#
#         date_ = basicBar_.getDateTime()
#
#         for aOrderPosiMFE in self.orderPostionMfeList:
#
#             # 2）计算mfe是否超过限额
#             aOrderPosi = aOrderPosiMFE['orderPosition']
#             symbol_ = aOrderPosi.symbol
#             vol_ = aOrderPosi.volume
#             # cost_ = aOrderPosi.cost
#             if symbol_ == 'SHFE.rb1805' and date_[0:10] == '2018-03-06':
#                 i = 1
#
#             if aOrderPosiMFE['MFE']:
#                 # if aOrderPosiMFE['MFE'] > cost_ * (profitRate):
#                 #     aOrderPosiMFE['enableTrailing'] = True
#                 #
#                 # aOrderPosiMFE.setdefault('enableTrailing', False)
#                 if aOrderPosiMFE['enableTrailing']:
#
#                     # #如果启动了跟踪止损，则
#                     # aOrderPosiMFE['enableBreakEven'] = True
#
#
#                     if aOrderPosi.positionSide == 'long':
#                         if basicBar_.getClose()<aOrderPosiMFE['HH']-self.__atrDS[-1]*backNATR:
#                             stopClearLongRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
#                                                             order_type=OrderType_Market,
#                                                             position_effect=PositionEffect_Close, price=0)
#
#                             # 更新orderPostionMfeList
#                             aOrderPosi.volume = 0
#
#                             # if symbol_=='SHFE.cu1901':
#                             #      i=1
#                             # self.loggerCons.info("%s barDate:%s long position breakEven stop", symbol_, date_)
#
#                     if aOrderPosi.positionSide == 'short':
#                         if basicBar_.getClose() > aOrderPosiMFE['LL'] + self.__atrDS[-1]*backNATR:
#                             stopclearShortRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
#                                                              order_type=OrderType_Market,
#                                                              position_effect=PositionEffect_Close, price=0)
#
#                             # 更新orderPostionMfeList
#                             aOrderPosi.volume = 0
#
#                             # if symbol_=='CZCE.CF805':
#                             #      i=1
#                             # self.loggerCons.info("%s barDate:%s short position breakEven stop", symbol_, date_)
#
#     def runTrailingStop(self, basicBar_,backNATR=1):
#         # profitRate 是指 收益率多少的时候，触发 trailingStop 止损。
#
#         date_ = basicBar_.getDateTime()
#
#         self.updateBarSinceEntry()
#
#         for aOrderPosi in self.orderPostionList:
#             self.__updateMFE(aOrderPosi, basicBar_)
#
#
#         for aOrderPosi in self.orderPostionList:
#
#             # 2）计算mfe是否超过限额
#
#             symbol_ = aOrderPosi.symbol
#             vol_ = aOrderPosi.volume
#             # cost_ = aOrderPosi.cost
#             if symbol_ == 'SHFE.rb1805' and date_[0:10] == '2018-03-06':
#                 i = 1
#
#             if aOrderPosi.mfe:
#                 # if aOrderPosiMFE['MFE'] > cost_ * (profitRate):
#                 #     aOrderPosiMFE['enableTrailing'] = True
#                 #
#                 # aOrderPosi.setdefault('enableTrailing', False)
#                 if aOrderPosi.enableTrailing:
#
#                     # #如果启动了跟踪止损，则
#                     # aOrderPosiMFE['enableBreakEven'] = True
#
#
#                     if aOrderPosi.positionSide == 'long':
#                         if basicBar_.getClose()<aOrderPosi.hh-self.__atrDS[-1]*backNATR:
#                             stopClearLongRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
#                                                             order_type=OrderType_Market,
#                                                             position_effect=PositionEffect_Close, price=0)
#
#                             # 更新orderPostionMfeList
#                             aOrderPosi.volume = 0
#
#                             # if symbol_=='SHFE.cu1901':
#                             #      i=1
#                             # self.loggerCons.info("%s barDate:%s long position breakEven stop", symbol_, date_)
#
#                     if aOrderPosi.positionSide == 'short':
#                         if basicBar_.getClose() > aOrderPosi.ll + self.__atrDS[-1]*backNATR:
#                             stopclearShortRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
#                                                              order_type=OrderType_Market,
#                                                              position_effect=PositionEffect_Close, price=0)
#
#                             # 更新orderPostionMfeList
#                             aOrderPosi.volume = 0
#
#
#         #清除点为0的 order
#         self.checkOrderPosiList()
#
#
#     def __updateMFE(self,posi_, basicBar_):
#         assert posi_ is not None
#         assert basicBar_ is not None
#
#
#
#         if posi_.barsSinceEntry > 0:
#             if posi_.barsSinceEntry == 1:
#                 posi_.hh = basicBar_.getHigh()
#                 posi_.ll = basicBar_.getLow()
#             else:
#                 posi_.hh = max(posi_.hh, basicBar_.getHigh())
#                 posi_.ll = min(posi_.ll, basicBar_.getLow())
#
#             if posi_.positionSide == 'long':
#                 posi_.mfe = posi_.hh - posi_.cost
#
#             if posi_.positionSide == 'short':
#                 posi_.mfe = posi_.cost - posi_.ll
#


class timeExitStrategy():
    def __init__(self,symbol,**kwargs):
        i=1
        self.symbol=symbol
        # context 来提供持仓的信息
        self.context = kwargs.get('context', None)
        self.exitTime=kwargs.get('exitTime', None)
        
        underLySym = commonHelpBylw.getMainContinContract(symbol)
        self.orderLog = loggerHelpbylw.getFileLogger(self.context.bTestID + '-' + underLySym + '-orderlog',
                                                'log\\' + self.context.bTestID + '\\' + underLySym + '-orderRecord.txt',
                                                mode_='a')


    #exitTime 提供什么时候出场。

    #返回值按时当前时间是 时间退场时间，告知主策略，本次bar，不用运行。
    def runbar4exitAfterTime(self, barTime):


        # if barTime[11:16] == self.exitTime:
        if barTime[11:16]>=self.exitTime and barTime[11:16]<'16:00':

            if self.context.normalLog is not None:
                self.context.normalLog.info('%s,%s',barTime,'timeExit in')


            symbolHolding = self.context.account().position(symbol=self.symbol, side=PositionSide_Long)
            if symbolHolding:


                vol_ = symbolHolding['volume']
                clearLongOrderRes = gm3HelpBylw.gmOrder.clearLong(self.symbol, vol_, 'time-cLong',barTime,ordrLog=self.orderLog,context=self.context)
                # self.upDateorderPosiListByClear(clearLongOrderRes[0])

            symbolHolding = self.context.account().position(symbol=self.symbol, side=PositionSide_Short)
            if symbolHolding:

                
                vol_ = symbolHolding['volume']
                clearShortOrderRes = gm3HelpBylw.gmOrder.clearShort(self.symbol, vol_, 'time-cShort',barTime,orderLog=self.orderLog,context=self.context)

                # self.upDateorderPosiListByClear(clearShortOrderRes[0])
            return True

        # if barTime[11:16]>self.exitTime and barTime[11:16]<'16:00':
        #     return True
        else:
            return False



#交割月不能进入 的退场
#普通投资者的合约不能进入交割月，所以其持仓要考察，是否即将进入交割月

def clearPositionByDeliveryDay(positions, nextTradeDate,context,moveOrderLog=None,orderType=2):
    # latestTradeDate 表示最近已经完成的交易日。比如20191107 11：00，那么此时20191107交易日没有完成，已经完成的最近的是20191106
    # moveOrderLog  这玩意 本来是为了将所有的移仓的动作都写文本，然后等待开盘时间到了后，从文本读取品种直接下单。但是后来发现
    # 总不是从内存写到本地，然后到时候又要从本地读到内存，那我干脆直接存到内存算了


    #本函数一定是在交易时间内运行,即在判为，查下下个交易日是不是要到交割月了。是的话，就平仓了。

    # 先查持仓

    if len(positions) <= 0:
        return

    from pandas.tseries.offsets import MonthBegin
    symbolList = []
    dt=context.now.strftime('%Y-%m-%d %H:%M:%S')
    for aposition in positions.values():
        aSymbol = aposition.getSymbol()
        symbolList.append(aSymbol)

    # symbolList.append('SHFE.fu2005')
    instuInfo = gm3HelpBylw.getInstumInfo(symbolList)


    for aposition in positions.values():
        aSymbol = aposition.getSymbol()
        # aSymbol='SHFE.fu2005'
        delistDate=instuInfo.loc[instuInfo['symbol']==aSymbol,'delisted_date'].iloc[0]


        deliveryMothDate=pd.Timestamp(delistDate)+MonthBegin(-1)
        deliveryMothDate=deliveryMothDate.strftime('%Y-%m-%d')


        nextTradeMothDate=nextTradeDate[0:8]+'01'
        delistDateStr=delistDate.strftime('%Y-%m-%d')


        clearFlag=False

        #对于像shfe.fu2005这种品种，到期日 都没有进入交割月的
        controlList=['SHFE.fu2005','SHFE.fu2009']

        if aSymbol not in controlList:
            if nextTradeMothDate >= deliveryMothDate:
                clearFlag=True
        else:
            if nextTradeDate >= delistDateStr:
                clearFlag=True
        if clearFlag:

            vol_ = aposition.Volume()
            side_ = aposition.getPositionSide()

            if side_ == PositionSide_Long:
                if orderType == 2:
                    gm3HelpBylw.gmOrder.clearLong(aSymbol, vol_, 'Delivery-cLong', dt, \
                                                  orderLog=context.orderLog,context=context)
                if orderType == 5:
                    gm3HelpBylw.gmOrder.clearLongWithNdang(aSymbol, vol_, 'Delivery-cLong', dt, \
                                                           orderLog=context.orderLog,context=context)
                if moveOrderLog is not None:

                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '卖平')

            if side_ == PositionSide_Short:
                if orderType == 2:
                    gm3HelpBylw.gmOrder.clearShort(aSymbol, vol_, 'Delivery-cShort', dt, \
                                                   orderLog=context.orderLog,context=context)
                if orderType == 5:
                    gm3HelpBylw.gmOrder.clearShortWithNdang(aSymbol, vol_, 'Delivery-cShort', dt, \
                                                            orderLog=context.orderLog,context=context)
                if moveOrderLog is not None:
                    # 平仓
                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '买平')

def clearPositionByDeliveryDay___back(positions, nextTradeDate,context,moveOrderLog=None,orderType=2):
    # latestTradeDate 表示最近已经完成的交易日。比如20191107 11：00，那么此时20191107交易日没有完成，已经完成的最近的是20191106
    # moveOrderLog  这玩意 本来是为了将所有的移仓的动作都写文本，然后等待开盘时间到了后，从文本读取品种直接下单。但是后来发现
    # 总不是从内存写到本地，然后到时候又要从本地读到内存，那我干脆直接存到内存算了


    #本函数一定是在交易时间内运行,即在判为，查下下个交易日是不是要到交割月了。是的话，就平仓了。

    # 先查持仓

    if len(positions) <= 0:
        return

    from pandas.tseries.offsets import MonthBegin
    symbolList = []
    dt=context.now.strftime('%Y-%m-%d %H:%M:%S')
    for aposition in positions:
        aSymbol = aposition.symbol
        symbolList.append(aSymbol)

    # symbolList.append('SHFE.fu2005')
    instuInfo = gm3HelpBylw.getInstumInfo(symbolList)


    for aposition in positions:
        aSymbol = aposition.symbol
        # aSymbol='SHFE.fu2005'
        delistDate=instuInfo.loc[instuInfo['symbol']==aSymbol,'delisted_date'].iloc[0]


        deliveryMothDate=pd.Timestamp(delistDate)+MonthBegin(-1)
        deliveryMothDate=deliveryMothDate.strftime('%Y-%m-%d')


        nextTradeMothDate=nextTradeDate[0:8]+'01'
        delistDateStr=delistDate.strftime('%Y-%m-%d')


        clearFlag=False

        #对于像shfe.fu2005这种品种，到期日 都没有进入交割月的
        controlList=['SHFE.fu2005','SHFE.fu2009']

        if aSymbol not in controlList:
            if nextTradeMothDate >= deliveryMothDate:
                clearFlag=True
        else:
            if nextTradeDate >= delistDateStr:
                clearFlag=True
        if clearFlag:

            vol_ = aposition['volume']
            side_ = aposition['side']

            if side_ == PositionSide_Long:
                if orderType == 2:
                    gm3HelpBylw.gmOrder.clearLong(aSymbol, vol_, 'Delivery-cLong', dt, \
                                                  orderLog=context.orderLog,context=context)
                if orderType == 5:
                    gm3HelpBylw.gmOrder.clearLongWithNdang(aSymbol, vol_, 'Delivery-cLong', dt, \
                                                           orderLog=context.orderLog,context=context)
                if moveOrderLog is not None:

                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '卖平')

            if side_ == PositionSide_Short:
                if orderType == 2:
                    gm3HelpBylw.gmOrder.clearShort(aSymbol, vol_, 'Delivery-cShort', dt, \
                                                   orderLog=context.orderLog,context=context)
                if orderType == 5:
                    gm3HelpBylw.gmOrder.clearShortWithNdang(aSymbol, vol_, 'Delivery-cShort', dt, \
                                                            orderLog=context.orderLog,context=context)
                if moveOrderLog is not None:
                    # 平仓
                    moveOrderLog.info("%s,%s,%s", aSymbol, vol_, '买平')