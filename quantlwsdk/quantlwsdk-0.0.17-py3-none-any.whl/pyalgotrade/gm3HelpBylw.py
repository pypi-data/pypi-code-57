# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:33:56 2018

@author: SH
"""
from gm.api import *
import pandas as pd
from pyalgotrade import config
from pandas.tseries.offsets import DateOffset
from pandas.tseries.offsets import Second
import datetime

from pyalgotrade import calendayBylw
from pyalgotrade.utils import gmEnum

from pyalgotrade import commonHelpBylw
from pyalgotrade import observer



from datetime import timezone
from datetime import timedelta
import time

## 用来获取当前主力合约的下一个主力合约的ID
#虽然这不太正确，因为下一个主力合约 是要根据当时成交量来判断的
#但是当前国内商品期货，主力合约都是固定的。比如 zc，的主力合约都是01，05，09 三个合约。所以
#主要针对这种情况
from pyalgotrade import loggerHelpbylw

month159CZCE = ['CZCE.TA', 'CZCE.SR', 'CZCE.CF', 'CZCE.OI', 'CZCE.MA',
                'CZCE.FG', 'CZCE.RM', 'CZCE.ZC', 'CZCE.SF', 'CZCE.SM']
month1510CZCE = ['CZCE.AP']

# 13个
month159DCE = ['DCE.A', 'DCE.B', 'DCE.C', 'DCE.CS', 'DCE.I', 'DCE.J',
               'DCE.JD', 'DCE.JM', 'DCE.L', 'DCE.M', 'DCE.P',
               'DCE.PP', 'DCE.V', 'DCE.Y', 'DCE.EG']

month1to12INE = ['INE.SC']


# 12个
# 铜  铝 锌 铅
month1to12SHFE = ['SHFE.AL', 'SHFE.CU', 'SHFE.PB', 'SHFE.ZN']
# 镍  锡 橡胶
month159SHFE = ['SHFE.SN', 'SHFE.NI', 'SHFE.RU', 'SHFE.FU', 'SHFE.SP']
# 螺纹 热卷
month1510SHFE = ['SHFE.HC', 'SHFE.RB']
# 沥青  黄金  白银
month612SHFE = ['SHFE.AU', 'SHFE.BU', 'SHFE.AG']

allCon = ['CFFEX.IC', 'CFFEX.IH', 'CFFEX.IF', 'CFFEX.T', 'CFFEX.TF']


def isUnderlyingSymbl(aSym):


    allUnderLyingSymbol=month159CZCE+month1510CZCE+month159DCE+\
                        month1to12INE+month1to12SHFE+month159SHFE+month1510SHFE+month612SHFE+allCon

    return aSym in allUnderLyingSymbol


def getNextContractID(currContractID):
    
  
    
    newContractID=''
   
    if 'CZCE.ZC' in currContractID:
        if currContractID[-2:]=='01':
            newContractID=currContractID[:-2]+'05'
        if currContractID[-2:]=='05':
            newContractID=currContractID[:-2]+'09'
        if currContractID[-2:]=='09':
            temp=str(int(currContractID[-3])+1)
            newContractID=currContractID[:-3]+temp+'01'
            
    return newContractID


# 即将相关系数矩阵 处理为 各个配对 排序的方式
def corrMatrixToPairs(corrMatrixOriginal):
    
    
    
    
    au_corr = corrMatrixOriginal.unstack()
    pairs_to_drop = set()
    cols = corrMatrixOriginal.columns
    for i in range(0, corrMatrixOriginal.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    au_corr = au_corr.drop(labels=pairs_to_drop).sort_values(ascending=False)
    au_corr.rename('corrCoeff',inplace=True)
    return au_corr
#    
    
'''

  #10g个
    month159CZCE=['CZCE.TA','CZCE.SR','CZCE.CF','CZCE.OI','CZCE.MA',
                      'CZCE.FG','CZCE.RM','CZCE.ZC','CZCE.SF','CZCE.SM']
    
    #13个
    month159DCE=['DCE.A','DCE.C','DCE.CS','DCE.I','DCE.J',
                      'DCE.JD','DCE.JM','DCE.L','DCE.M','DCE.P',
                      'DCE.PP','DCE.V','DCE.Y']
    
    #12个
   #铜  铝 锌 铅
    month1to12SHFE=['SHFE.AL','SHFE.CU','SHFE.PB','SHFE.ZN']
    
    #镍  锡 橡胶
    month159SHFE=['SHFE.SN','SHFE.NI','SHFE.RU']
    
    #螺纹 热卷
    month1510SHFE=['SHFE.HC','SHFE.RB']
    
    #沥青  黄金  白银
    month612SHFE=['SHFE.AU','SHFE.BU','SHFE.AG']

    
    
'''






#
#'''
#
##取出指定时间内正在市场上交易的合约。
#
#'''
#
#def getSomeContractBylw(month159CZCE,month159DCE,\
#                        month1to12SHFE,month159SHFE,month1510SHFE,month612SHFE,\
#                        sDateTime,eDateTime):
#    
#    
#    
#    
#    
#    
#    currAllFutureContract=get_instruments(symbols=None, exchanges=None, sec_types=[SEC_TYPE_FUTURE], names=None, skip_suspended=True, skip_st=True, fields='symbol,exchange,sec_id,listed_date,delisted_date', df=True)
#    
#    if sDateTime and eDateTime:
#        currAllFutureContract=currAllFutureContract\
#        [~((currAllFutureContract['listed_date'].astype(str)>eDateTime)|\
#         (currAllFutureContract['delisted_date'].astype(str)<sDateTime))]
#    
#    tempContract=currAllFutureContract
#    
#    finalContract=[]
#    
#    for inx, row in tempContract.iterrows():
#        
#        currVirtualContract=''
#        if row['exchange']=='CZCE':
#            currVirtualContract=row['exchange']+'.'+row['sec_id'][:-3].upper()
#        else:
#            currVirtualContract=row['exchange']+'.'+row['sec_id'][:-4].upper()
#    
#        if row['exchange']=='SHFE':
#            i=1
#            
#        if  currVirtualContract in month159CZCE+month159DCE+month159SHFE:
#            if row['sec_id'][-2:] in ['01','05','09']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month1to12SHFE:
#            if row['sec_id'][-2:] in ['01','02','03','04','05','06']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month1510SHFE:
#            if row['sec_id'][-2:] in ['01','05','10']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month612SHFE:
#            if row['sec_id'][-2:] in ['06','12']:
#                finalContract.append(row['symbol'])
#                
#    i=1
#    return finalContract
#               
      
    
'''

取出指定时间内正在市场上交易的合约。

'''
#
#def getSomeContract2Bylw(month159,month1to12,month1510,month612,\
#                        sDateTime,eDateTime):
#    
#    
#    
#    
#    
#    
#    currAllFutureContract=get_instruments(symbols=None, exchanges=None, sec_types=[SEC_TYPE_FUTURE], names=None, skip_suspended=True, skip_st=True, fields='symbol,exchange,sec_id,listed_date,delisted_date', df=True)
#    
#    if sDateTime and eDateTime:
#        currAllFutureContract=currAllFutureContract\
#        [~((currAllFutureContract['listed_date'].astype(str)>eDateTime)|\
#         (currAllFutureContract['delisted_date'].astype(str)<sDateTime))]
#    
#    tempContract=currAllFutureContract
#    
#    finalContract=[]
#    
#    for inx, row in tempContract.iterrows():
#        
#        currVirtualContract=''
#        if row['exchange']=='CZCE':
#            currVirtualContract=row['exchange']+'.'+row['sec_id'][:-3].upper()
#        else:
#            currVirtualContract=row['exchange']+'.'+row['sec_id'][:-4].upper()
#    
#        if row['exchange']=='SHFE':
#            i=1
#        if row['sec_id'][:-4]=='cu':
#            i=1
#            
#            
#        if  currVirtualContract in month159:
#            if row['sec_id'][-2:] in ['01','05','09']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month1to12:
#            if row['sec_id'][-2:] in ['01','03','05','07','09','11']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month1510:
#            if row['sec_id'][-2:] in ['01','05','10']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month612:
#            if row['sec_id'][-2:] in ['06','12']:
#                finalContract.append(row['symbol'])
#                
#    i=1
#    return finalContract
#               




'''

取出到当前时间点所有历史上出现过的沪深A股

'''
def getHSAStockBylw():


    
    # 取出所有沪深A股。 掘金上，没法直接取，只能绕一绕。
    #取出最新时间时刻的 沪深300股票。
    
    
    #下面函数取所有交易所的所有标的，查掘金文档知道，支持的交易所只有国内的
    #上交所	SHSE
    #深交所	SZSE
    #中金所	CFFEX
    #上期所	SHFE
    #大商所	DCE
    #郑商所	CZCE
    #上海国际能源交易中心	INE
    #所以限定取股票后基本上取的就是沪深2市的股票了。
    stock300=get_instruments(symbols=None, exchanges=None, sec_types=[SEC_TYPE_STOCK], names=None, skip_suspended=False, skip_st=False, fields='symbol,sec_type,exchange,sec_id,sec_name,listed_date,delisted_date,is_suspended', df=True)
    
    
    #清除b股
    aStock=stock300.loc[(stock300['sec_id'].str[0]!='2') & (stock300['sec_id'].str[0]!='9')]
    
    
    
    return list(aStock['symbol'].values)




    

def getExchangeFromGmSymbol(gmSymbol):
    return gmSymbol.split('.')[0]

'''

获取指定时间段内，某些品种的在 上市交易的 符合 要求的合约。

'''

def getContractsByUnderlyingSymbols(symbolsCode,sDateTime,eDateTime):
    
    #sDateTime是字符串类型。只有日期
    #symbolsCode 是标的资产的代码。是个list
    
          #10g个

    exchangelist=[]
    for asym in symbolsCode:
        exchangelist.append(getExchangeFromGmSymbol(asym))
    exchangelist=list(set(exchangelist))


    month159=month159CZCE+month159DCE+month159SHFE
    month1to12=month1to12SHFE+month1to12INE
    month1510=month1510SHFE+month1510CZCE
    month612=month612SHFE
    
    currAllFutureContract=get_instruments(symbols=None, exchanges=exchangelist, sec_types=[SEC_TYPE_FUTURE], names=None, skip_suspended=True, skip_st=True, fields='symbol,exchange,sec_id,listed_date,delisted_date', df=True)

    currAllFutureContract['listed_date']=currAllFutureContract['listed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['listed_date'] = currAllFutureContract['listed_date'].str[0:10]
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].str[0:10]


    if sDateTime and eDateTime:

     currAllFutureContract=currAllFutureContract[(currAllFutureContract['listed_date']<=sDateTime) & \
     (currAllFutureContract['delisted_date']>=eDateTime)]
    
    tempContract=currAllFutureContract
    

    finalDf=pd.DataFrame(columns=currAllFutureContract.columns)
    
    for inx, row in tempContract.iterrows():
        underLyingSymbol=commonHelpBylw.getMainContinContract(row['symbol'])
    

        #确认当前品种是我们需要的品种
        if underLyingSymbol in symbolsCode:
            if  underLyingSymbol in month159:
                if row['sec_id'][-2:] in ['01','05','09']:

                    finalDf.loc[finalDf.shape[0]]=row
            if  underLyingSymbol in month1to12:
                if row['sec_id'][-2:] in ['01','03','05','07','09','11']:

                    finalDf.loc[finalDf.shape[0]] = row
            if  underLyingSymbol in month1510:
                if row['sec_id'][-2:] in ['01','05','10']:

                    finalDf.loc[finalDf.shape[0]] = row
            if  underLyingSymbol in month612:
                if row['sec_id'][-2:] in ['06','12']:

                    finalDf.loc[finalDf.shape[0]] = row
            if underLyingSymbol in allCon:

                finalDf.loc[finalDf.shape[0]] = row
                
    i=1
    return finalDf




#这里和上面函数的差别在于，这里不会去将合约挑出个1，5，9之类的。
def getAllCanTradeContractsByUnderlyingSymbols(symbolsCode, sDateTime, eDateTime):
    # sDateTime是字符串类型。只有日期
    # symbolsCode 是标的资产的代码。是个list

    # 10g个

    exchangelist = []
    for asym in symbolsCode:
        exchangelist.append(getExchangeFromGmSymbol(asym))
    exchangelist = list(set(exchangelist))

    month159 = month159CZCE + month159DCE + month159SHFE
    month1to12 = month1to12SHFE + month1to12INE
    month1510 = month1510SHFE + month1510CZCE
    month612 = month612SHFE

    currAllFutureContract = get_instruments(symbols=None, exchanges=exchangelist, sec_types=[SEC_TYPE_FUTURE],
                                            names=None, skip_suspended=True, skip_st=True,
                                            fields='symbol,exchange,sec_id,listed_date,delisted_date', df=True)

    currAllFutureContract['listed_date'] = currAllFutureContract['listed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['listed_date'] = currAllFutureContract['listed_date'].str[0:10]
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    currAllFutureContract['delisted_date'] = currAllFutureContract['delisted_date'].str[0:10]

    if sDateTime and eDateTime:
        currAllFutureContract = currAllFutureContract[(currAllFutureContract['listed_date'] <= sDateTime) & \
                                                      (currAllFutureContract['delisted_date'] >= eDateTime)]

    tempContract = currAllFutureContract

    finalDf = pd.DataFrame(columns=currAllFutureContract.columns)

    for inx, row in tempContract.iterrows():
        underLyingSymbol = commonHelpBylw.getMainContinContract(row['symbol'])

        # 确认当前品种是我们需要的品种
        if underLyingSymbol in symbolsCode:

                finalDf.loc[finalDf.shape[0]] = row

    i = 1
    return finalDf


'''

价差价比计算

apair 可以是元组，可以是list
'''

def ratioSpreadCal(aPair,astartTime,aendTime):
    aData= history(symbol=aPair[0], frequency='1d', start_time=astartTime,end_time=aendTime, fields='close,symbol,eob', df=True)
    
    if aData.empty:
        print(aPair[0]+' is empty')
        return pd.DataFrame()
    
    aData.rename(columns={"close": aPair[0]},inplace=True)
    
    
    
    bData= history(symbol=aPair[1], frequency='1d', start_time=astartTime,end_time=aendTime, fields='close,symbol,eob', df=True)
    if bData.empty:
        print(aPair[1]+' is empty')
        return pd.DataFrame()
        
    bData.rename(columns={"close": aPair[1]},inplace=True)
    
    
    concatData=pd.merge(aData,bData,on='eob') 
        
    
    if aPair[0]=='CZCE.SM' and aPair[1]=='DCE.J':
        iiid=1
    
    concatData[aPair[0]+'-'+aPair[1]]=concatData[aPair[0]]-concatData[aPair[1]]
    concatData[aPair[0]+'/'+aPair[1]]=concatData[aPair[0]]/concatData[aPair[1]]
    
    return concatData
        
        

def getHQDataFromGm(symbol,sDateTime,eDateTime,fields=None):


    

    aaa=history(symbol=symbol,frequency='60s',start_time=sDateTime,end_time=eDateTime,fields=fields,df=True)
    return aaa




#
# # 本函数，根据gm下单结果（开仓和平仓下单），来增加或者减少list中的orderPosition对象
# #
# def updateOrderPositionMFElist(orderRe,strategyObj):
#     if orderRe is  None:
#         return
#     position_effect = orderRe[0]['position_effect']
#     position_side = orderRe[0]['position_side']
#     volNum_ = orderRe[0]['filled_volume']
#     symbol_ = orderRe[0]['symbol']
#
#     if position_side == PositionSide_Long:
#         positionSideStr = 'long'
#     if position_side == PositionSide_Short:
#         positionSideStr = 'short'
#
#
#     # 开仓
#     if position_effect == PositionEffect_Open:
#
#         cost_ = orderRe[0]['filled_vwap']
#         commission_ = 0
#
#         aOrderPosition = BaseOrderHoldingPostion(symbol_, positionSideStr, volNum_, cost_,
#                                                  commission=commission_)
#         aOrderPosition.barsSinceEntry = -1  # 这里是因为 真正成交是下个bar成交的
#         adict = {}
#         adict['strategyOrderID'] = None
#         adict['orderPosition'] = aOrderPosition
#         adict['HH'] = None
#         adict['LL'] = None
#         adict['MFE'] = None
#
#         if symbol_ == strategyObj.symbol:
#             # self.orderPostionMfeList.append(adict)
#             strategyObj.orderPostionMfeList.append(adict)
#         else:
#             # 访问其他合约的 策略对象
#             strategyObj.allSymStrategy[symbol_].orderPostionMfeList.append(adict)
#
#     # 平仓
#     if position_effect == PositionEffect_Close:
#
#         if symbol_ == strategyObj.symbol:
#             for aOrderPosi in reversed(strategyObj.orderPostionMfeList):
#                 if aOrderPosi['orderPosition'].positionSide == positionSideStr:
#
#                     if aOrderPosi['orderPosition'].volume >= volNum_:
#                         aOrderPosi['orderPosition'].volume = aOrderPosi['orderPosition'].volume - volNum_
#                         break
#                     else:
#                         aOrderPosi['orderPosition'].volume = 0
#                         volNum_ = volNum_ - aOrderPosi['orderPosition'].volume
#
#         else:
#             for aOrderPosi in reversed(rangBreakSys.allSymStrategy[symbol_].orderPostionMfeList):
#                 if aOrderPosi['orderPosition'].positionSide == positionSideStr:
#
#                     if aOrderPosi['orderPosition'].volume >= volNum_:
#                         aOrderPosi['orderPosition'].volume = aOrderPosi['orderPosition'].volume - volNum_
#                         break
#                     else:
#                         aOrderPosi['orderPosition'].volume = 0
#                         volNum_ = volNum_ - aOrderPosi['orderPosition'].volume
#


def getTradeMsg(OrderRes):


    # if OrderRes[0].ord_rej_reason == gmEnum.OrderRejectReason_Unknown:
    #     tradeMsg = 'normal'
    if OrderRes[0].ord_rej_reason == gmEnum.OrderRejectReason_NoEnoughCash :
        tradeMsg = 'NoEnoughCash'
        return  tradeMsg

class gmOrder():
    
    # orderLog=None
    clearOrderEvent = observer.Event()

    aOrderConrolOBj=None   #用来标记是否开启延时委托。比如15:00发出的委托，肯定是报单出去不，只能是存在本地，表明是代报状态。下一个交易日
    #一开始，就要报出去。

    def __init__(self):

        self.i=1

    # @classmethod
    # def reverseClear(cls,clearFun,symbol_,signalName,dt,**kwargs):
    #     context = kwargs.get('context', None)
    #     # 空头持仓要平掉
    #     symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
    #     if symbolHolding:
    #         vol1_ = symbolHolding['volume']
    #         context.clearPositionSignalNames = ['all']
    #         clearShortOrderRes = clearFun(symbol_, vol1_, signalName, dt)
    # @classmethod
    # def _getALog(cls,bTestID,underLySym):
    #     # loggerHelpbylw.getFileLogger(self.context.bTestID + '-' + self.underLySym + '-orderlog',
    #     #                                     'log\\'+self.context.bTestID+'\\' + self.underLySym + '-orderRecord.txt',mode_='a')
    #
    #     aLog=loggerHelpbylw.getFileLogger(bTestID + '-' + underLySym + '-orderlog',
    #                                  'log\\' + bTestID + '\\' + underLySym + '-orderRecord.txt',
    #                                  mode_='a')
    #     return aLog

    @classmethod
    def _marketOrderControl(cls,context,symbol_,dt):

        if context.is_live_model():
            exchangeID=symbol_.split('.')[0]
            orderTime=dt[11:]

            if exchangeID in ['SHFE','CFFEX','DCE','CZCE']:
                ulying_asset = commonHelpBylw.getMainContinContract(symbol_)
                jiheOrderTime = config.jiheOrderTimeDict[ulying_asset]
            else:
                ulying_asset=symbol_



            if orderTime>=jiheOrderTime[0] and orderTime<=jiheOrderTime[1]:
                isinJiHeTime=True
            else:
                isinJiHeTime = False




            if exchangeID=='SHFE'  or isinJiHeTime:
                pricesDF=getInstumInfo(symbol_,fields='symbol,trade_date,upper_limit,lower_limit')

                return True,pricesDF
            else:
                return False,None
        else:
            return False, None

                # upperLimitPrice=pricesDF['upper_limit'].iloc[0]

    #orderType=1表示限价单，orderType=2表示市价委托
    @classmethod
    def openLong(cls,symbol_,vol_,signalName,dt,clearReverse=False,orderType=2,**kwargs):
        context = kwargs.get('context', None)
        price = kwargs.get('price', None)
        # if context.is_live_model()and orderType==2:
        #     exchangeID=symbol_.split('.')[0]
        #     if exchangeID=='SHFE':
        #         pricesDF=getInstumInfo(symbol_,fields='symbol,trade_date,upper_limit,lower_limit')
        if orderType==2:
            changeOrderType,pricesDF=cls._marketOrderControl(context,symbol_,dt)

            if changeOrderType:
                upperLimitPrice=pricesDF['upper_limit'].iloc[0]
                return cls.openLong(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1,price=upperLimitPrice, **kwargs)

        #如果是限价单。则要读取
        if clearReverse:
            # 空头持仓要平掉
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
            if symbolHolding and symbolHolding['available']>0:
                vol1_ = symbolHolding['available']
                context.clearPositionSignalNames = ['allShort']
                # 剔除掉price,因为要用市价了
                if 'price' in kwargs:
                    del kwargs['price']
                clearShortOrderRes = cls.clearShort(symbol_, vol1_, 'cshort',dt,orderType=2,**kwargs)

            # cls.reverseClear(cls.clearShort,symbol_,'cshort',dt,**kwargs)

        orderLog = kwargs.get('orderLog', None)
        # 限价单的话，就必须提供委托价格
        if orderType == 1:

            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'ol',order_volume,\
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Buy,
                                                          'order_type':OrderType_Limit,
                                                          'position_effect':PositionEffect_Open,
                                                          'price':price}):
                    return
            openLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
                                            order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=price)

        if orderType==2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'ol',order_volume,\
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Buy,
                                                          'order_type':OrderType_Market,
                                                          'position_effect':PositionEffect_Open,
                                                          'price':0}):
                    sigMsg=signalName+'-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
                                            order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)
        # print(openLongOrderRes)
        tradeMsg = getTradeMsg(openLongOrderRes)


        # if writeOrderLog:

        if orderLog is not None:

            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName
            # cls.orderLog.info("%s,%s,%d,%d,%d,%s",dt, symbol_,vol_,OrderSide_Buy,PositionEffect_Open,signalName)
            # cls.orderLog.info("%s,%s,%s", dt, symbol_,sigMsg+'-'+symbol_)
            orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
        return openLongOrderRes

    @classmethod
    def openShort(cls, symbol_, vol_,signalName,dt,clearReverse=False,orderType=2,**kwargs):
        context = kwargs.get('context', None)
        price = kwargs.get('price', None)
        if orderType == 2:
            changeOrderType, pricesDF = cls._marketOrderControl(context, symbol_, dt)

            if changeOrderType:
                lowerLimitPrice=pricesDF['lower_limit'].iloc[0]
                return cls.openShort(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1,price=lowerLimitPrice, **kwargs)
        if clearReverse:
            # 多头持仓要平掉
            context = kwargs.get('context', None)
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
            if symbolHolding and symbolHolding['available'] > 0:
                vol1_ = symbolHolding['available']
                context.clearPositionSignalNames = ['allLong']
                # 剔除掉price,因为要用市价了
                if 'price' in kwargs:
                    del kwargs['price']
                clearLongOrderRes = cls.clearLong(symbol_, vol1_, 'clong',dt,orderType=2,**kwargs)
            # cls.reverseClear(cls.clearLong, symbol_, 'clong', dt,**kwargs)
        orderLog = kwargs.get('orderLog', None)
        if orderType==2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'os',order_volume,\
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Sell,
                                                          'order_type':OrderType_Market,
                                                          'position_effect':PositionEffect_Open,
                                                          'price':0}):
                    return

            openShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
                                            order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

        if orderType==1:


            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'os',order_volume,\
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Sell,
                                                          'order_type':OrderType_Limit,
                                                          'position_effect':PositionEffect_Open,
                                                          'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
                                            order_type=OrderType_Limit, position_effect=PositionEffect_Open, price=price)

        tradeMsg = getTradeMsg(openShortOrderRes)

        # if writeOrderLog:
        if orderLog is not None:


            if tradeMsg is not None:
                sigMsg = signalName + '-' + tradeMsg
            else:
                sigMsg = signalName

            # cls.orderLog.info("%s,%s,%d,%d,%d,%s",dt, symbol_,vol_,OrderSide_Sell,PositionEffect_Open,signalName)
            # cls.orderLog.info("%s,%s,%s", dt, symbol_, sigMsg+'-'+symbol_)
            orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
        return openShortOrderRes

    @classmethod
    def clearLong(cls, symbol_, vol_,signalName,dt,clearSignals=['allLong'],orderType=2,**kwargs):

        context = kwargs.get('context', None)

        # #查询是否有持仓，且是可用持仓
        # symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
        # if symbolHolding and symbolHolding['available'] < vol_:
        #     return

        orderLog = kwargs.get('orderLog', None)

        if orderType == 2:
            changeOrderType, pricesDF = cls._marketOrderControl(context, symbol_, dt)

            if changeOrderType:
                lower_limit = pricesDF['lower_limit'].iloc[0]
                return cls.clearLong(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1,
                                    price=lower_limit, **kwargs)
        # 限价单的话，就必须提供委托价格
        if orderType == 1:
            price = kwargs.get('price', None)

            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'cl', order_volume, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Sell,
                                                              'order_type': OrderType_Limit,
                                                              'position_effect': PositionEffect_Close,
                                                              'price': price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            clearLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
                                             order_type=OrderType_Limit, position_effect=PositionEffect_Close, price=price)
        if orderType==2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'cl', order_volume, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Sell,
                                                              'order_type': OrderType_Market,
                                                              'position_effect': PositionEffect_Close,
                                                              'price': 0}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            clearLongOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Sell,
                                             order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)
        if orderLog is not None:

            orderLog.info("%s,%s,%s", dt, symbol_, signalName + '-' + symbol_+'-'+str(price))
        # cls.clearOrderEvent.emit(clearLongOrderRes[0],clearSignals)
        return clearLongOrderRes

    @classmethod
    def clearShort(cls, symbol_, vol_,signalName,dt,clearSignals=['allShort'],orderType=2,**kwargs):
        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
             # # 查询是否有持仓，且是可用持仓
        # symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
        # if symbolHolding and symbolHolding['available'] < vol_:
        #     return

        if orderType == 2:
            changeOrderType, pricesDF = cls._marketOrderControl(context, symbol_, dt)

            if changeOrderType:
                upper_limit = pricesDF['upper_limit'].iloc[0]
                return cls.clearShort(symbol_, vol_, signalName, dt, clearReverse=False, orderType=1,
                                     price=upper_limit, **kwargs)
        if orderType == 2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'cs', order_volume, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Buy,
                                                              'order_type': OrderType_Market,
                                                              'position_effect': PositionEffect_Close,
                                                              'price': price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            clearShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
                                            order_type=OrderType_Market, position_effect=PositionEffect_Close, price=0)
        if orderType == 1:
            price = kwargs.get('price', None)
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'cs', order_volume, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'volume': vol_,
                                                              'side': OrderSide_Buy,
                                                              'order_type': OrderType_Limit,
                                                              'position_effect': PositionEffect_Close,
                                                              'price': price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            clearShortOrderRes = order_volume(symbol=symbol_, volume=vol_, side=OrderSide_Buy,
                                              order_type=OrderType_Limit, position_effect=PositionEffect_Close,
                                                  price=price)

        if orderLog is not None:
        # if writeOrderLog:

            # cls.orderLog.info("%s,%s,%d,%d,%d,%s",dt, symbol_,vol_,OrderSide_Buy,PositionEffect_Close,signalName)
            # cls.orderLog.info("%s,%s,%s", dt, symbol_, signalName+'-'+symbol_)
            orderLog.info("%s,%s,%s", dt, symbol_, signalName + '-' + symbol_+'-'+str(price))
        # cls.clearOrderEvent.emit(clearShortOrderRes[0], clearSignals)
        return clearShortOrderRes



    @classmethod
    def clearLongAllPo(cls, symbol_,  signalName,dt,orderType=2,**kwargs):

        context = kwargs.get('context', None)
        symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
        if symbolHolding and symbolHolding['available'] > 0:
            vol1_ = symbolHolding['available']
            clearLongOrderRes = cls.clearLong(symbol_,vol1_,signalName,dt,orderType=orderType,**kwargs)
            return clearLongOrderRes

    @classmethod
    def clearShortAllPo(cls, symbol_, signalName,dt,orderType=2,**kwargs):

        context = kwargs.get('context', None)
        symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
        if symbolHolding and symbolHolding['available'] > 0:
            vol1_ = symbolHolding['available']
            clearShortOrderRes = cls.clearShort(symbol_, vol1_, signalName,dt,orderType=orderType,**kwargs)
            return clearShortOrderRes

    @classmethod

    #这个是平掉所有 可用持仓，被占用的持仓是不平的
    def clearAllAvailPo(cls,signalName, dt, orderType=2, **kwargs):

        context = kwargs.get('context', None)

        symbolHolding = context.account().positions()
        for aposi in symbolHolding:
            if aposi['available'] > 0:
                vol1_ = aposi['available']
                symbol_=aposi['symbol']

                if aposi['side']==2:
                    clearShortOrderRes = cls.clearShort(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                    return clearShortOrderRes
                if aposi['side']==1:
                    clearLongOrderRes = cls.clearLong(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                    return clearLongOrderRes

    @classmethod

    #这个是平掉所有可用持仓+委托占用的要撤单掉。再平仓
    def clearAllPo(cls, signalName, dt, orderType=2, **kwargs):

        context = kwargs.get('context', None)
        waitOrderS = get_unfinished_orders()
        for aOrder in waitOrderS:
            orderDict = {}

            orderDict['cl_ord_id'] = aOrder.cl_ord_id
            orderDict['account_id'] = aOrder.account_id
            # order_cancel(orderDict)

            if aOrder.position_effect==1:
                continue
            else:
                symbol_=aOrder.symbol
                if aOrder.side==1: #买平，则持仓为空
                    pSide=2
                else:
                    pSide=1


            symbolHolding = context.account().position(symbol_,pSide)
            vol1_=symbolHolding['available']+aOrder.volume-aOrder.filled_volume
            order_cancel(orderDict)

            if pSide == 2:
                clearShortOrderRes = cls.clearShort(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                return clearShortOrderRes
            if pSide == 1:
                clearLongOrderRes = cls.clearLong(symbol_, vol1_, signalName, dt, orderType=orderType, **kwargs)
                return clearLongOrderRes




    @classmethod
    # 这函数 股票是可以这么弄，但是期货就不对了。期货要有合约乘数，保证金比例等信息
    # def openLongWithCash(cls, symbol_, cash_, upPriceV, cusComRatio, signalName, clearReverse=False):
    def openLongWithCash(cls, symbol_, cash_,signalName,dt,clearReverse=False,orderType=2,**kwargs):
        
        #clearReverse 表示是否平掉反向的持仓。即开多，那么已有的空头持仓要平仓。
        
        # realVol = int(cash_ / (100 * upPriceV * (1 + cusComRatio))) * 100

        # openLongOrderRes = order_volume(symbol=symbol_, volume=realVol, side=OrderSide_Buy,
        #                                 order_type=OrderType_Market, position_effect=PositionEffect_Open, price=0)

        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        price = kwargs.get('price', None)
        if orderType == 2:
            changeOrderType, pricesDF = cls._marketOrderControl(context, symbol_, dt)

            if changeOrderType:
                upper_limit = pricesDF['upper_limit'].iloc[0]
                return cls.openLongWithCash(symbol_, cash_, signalName, dt, clearReverse=False, orderType=1,
                                    price=upper_limit, **kwargs)

        if clearReverse:

            # 空头持仓要平掉
            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Short)
            if symbolHolding and symbolHolding['available'] > 0:
                vol1_ = symbolHolding['available']
                context.clearPositionSignalNames = ['allShort']
                # 剔除掉price,因为要用市价了
                if 'price' in kwargs:
                    del kwargs['price']
                clearShortOrderRes = cls.clearShort(symbol_, vol1_, 'cshort',dt,orderType=2,**kwargs)
            # cls.reverseClear(cls.clearShort, symbol_, 'cshort', dt,**kwargs)

        if orderType==2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'ol', order_value, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'value': cash_,
                                                              'side': OrderSide_Buy,
                                                              'order_type': OrderType_Market,
                                                              'position_effect': PositionEffect_Open,
                                                              'price': 0}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openLongOrderRes=order_value(symbol=symbol_, value=cash_, price=0, side=OrderSide_Buy, order_type=OrderType_Market,
                        position_effect=PositionEffect_Open)
        if orderType==1:

            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'ol', order_value, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'value': cash_,
                                                              'side': OrderSide_Buy,
                                                              'order_type': OrderType_Limit,
                                                              'position_effect': PositionEffect_Open,
                                                              'price': price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openLongOrderRes = order_value(symbol=symbol_, value=cash_, price=price, side=OrderSide_Buy,
                                           order_type=OrderType_Limit,
                                           position_effect=PositionEffect_Open)


        tradeMsg=getTradeMsg(openLongOrderRes)

        # if writeOrderLog:

        if orderLog is not None:
            # cls.orderLog.info("%s,%s,%f,%d,%d,%s",dt, symbol_,cash_,OrderSide_Buy,PositionEffect_Open,signalName)

            if tradeMsg is not None:
                sigMsg=signalName+'-'+tradeMsg
            else:
                sigMsg = signalName

            # cls.orderLog.info("%s,%s,%s", dt, symbol_, sigMsg+'-'+symbol_)
            orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
        return openLongOrderRes

    @classmethod
    # vol_是手数
    def openShortWithCash(cls, symbol_, cash_,signalName,dt,clearReverse=False,orderType=2,**kwargs):

        context = kwargs.get('context', None)
        orderLog = kwargs.get('orderLog', None)
        price = kwargs.get('price', None)
        if orderType == 2:
            changeOrderType, pricesDF = cls._marketOrderControl(context, symbol_, dt)

            if changeOrderType:
                lower_limit = pricesDF['lower_limit'].iloc[0]
                return cls.openLongWithCash(symbol_, cash_, signalName, dt, clearReverse=False, orderType=1,
                                            price=lower_limit, **kwargs)
        if clearReverse:
            # 多头持仓要平掉

            symbolHolding = context.account().position(symbol=symbol_, side=PositionSide_Long)
            if symbolHolding and symbolHolding['available'] > 0:
                vol1_ = symbolHolding['available']
                context.clearPositionSignalNames = ['allLong']
                # 剔除掉price,因为要用市价了
                if 'price' in kwargs:
                    del kwargs['price']
                clearLongOrderRes = cls.clearLong(symbol_, vol1_, 'clong',dt,orderType=2,**kwargs)
            # cls.reverseClear(cls.clearLong, symbol_, 'clong', dt,**kwargs)


        if orderType==2:
            price=0
            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'os', order_value, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'value': cash_,
                                                              'side': OrderSide_Sell,
                                                              'order_type': OrderType_Market,
                                                              'position_effect': PositionEffect_Open}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openShortOrderRes = order_value(symbol=symbol_, value=cash_, price=0, side=OrderSide_Sell,order_type=OrderType_Market,
                                           position_effect=PositionEffect_Open)
        if orderType==1:

            if cls.aOrderConrolOBj is not None:
                if cls.aOrderConrolOBj.controlByOrderTime(dt, symbol_,'os', order_value, \
                                                          funkargs={
                                                              'symbol': symbol_,
                                                              'value': cash_,
                                                              'side': OrderSide_Sell,
                                                              'order_type': OrderType_Limit,
                                                              'position_effect': PositionEffect_Open,
                                                          'price':price}):
                    sigMsg = signalName + '-delay'
                    orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))
                    return
            openShortOrderRes = order_value(symbol=symbol_, value=cash_, price=price, side=OrderSide_Sell,
                                            order_type=OrderType_Limit,
                                            position_effect=PositionEffect_Open)

        tradeMsg=getTradeMsg(openShortOrderRes)

        if orderLog is not None:
        # if writeOrderLog:


            if tradeMsg is not None:
                sigMsg=signalName+'-'+tradeMsg
            else:
                sigMsg = signalName

            # cls.orderLog.info("%s,%s,%f,%d,%d,%s",dt, symbol_,cash_,OrderSide_Sell,PositionEffect_Open,signalName
            # cls.orderLog.info("%s,%s,%s", dt, symbol_, sigMsg+'-'+symbol_)
            orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_+'-'+str(price))

        return openShortOrderRes

        # orderType=1表示限价单，orderType=2表示市价委托


    def fengexian(self):
        i=1
    @classmethod
    def openLongWithNdang(cls, symbol_, vol_, signalName, dt, clearReverse=False, pattern='ACITVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_,'sell',0)# 开多是买，对手是卖。
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_,'buy',0) # 开多是买，我方是买。

        # 限价单
        openLongOrderRes=cls.openLong(symbol_,vol_,signalName,dt,clearReverse=clearReverse,orderType=1,price=price,**kwargs)

        return openLongOrderRes

    @classmethod
    def openShortWithNdang(cls, symbol_, vol_, signalName, dt, clearReverse=False,  pattern='ACITVE1', **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)  # 开空是卖，对手是买。
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)  # 开空是卖，我方是卖。

        # 限价单
        openShortOrderRes = cls.openShort(symbol_, vol_, signalName, dt, clearReverse=clearReverse, orderType=1, price=price,
                                        **kwargs)

        return openShortOrderRes




    @classmethod
    def clearLongAllPoWithNdang(cls, symbol_, signalName, dt, pattern='ACITVE1', **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)


        clearLongOrderRes = cls.clearLongAllPo(symbol_, signalName, dt, orderType=1,price=price, **kwargs)
        return clearLongOrderRes

    @classmethod
    def clearShortAllPoWithNdang(cls, symbol_, signalName, dt, pattern='ACITVE1', **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        clearShortOrderRes = cls.clearShortAllPo(symbol_, signalName, dt, orderType=1,price=price, **kwargs)
        return clearShortOrderRes

    @classmethod
    def openLongWithCashWithNdang(cls, symbol_, cash_, signalName, dt, clearReverse=False, pattern = 'ACTIVE1', **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        openLongOrderRes=cls.openLongWithCash(symbol_, cash_, signalName, dt, clearReverse=clearReverse, \
                                                       orderType=1,price=price, **kwargs)

        return openLongOrderRes

    @classmethod
    # vol_是手数
    def openShortWithCashWithNdang(cls, symbol_, cash_, signalName, dt, clearReverse=False, pattern = 'ACTIVE1', **kwargs):
        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        openShortOrderRes=cls.openShortWithCash(symbol_, cash_, signalName, dt, clearReverse=clearReverse,\
                                                orderType=1,price=price, **kwargs)
        return openShortOrderRes
    # 用具体的档位价格来下限价单。
    # ACTIVE1 表示用对手价1档下限价单，POSITIVE1表示用我方价的1档下限价单
    @classmethod
    def clearLongWithNdang(cls, symbol_, vol_, signalName, dt, clearSignals=['allLong'], pattern='ACTIVE1',
                           **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)

        clearLongOrderRes = cls.clearLong(symbol_, vol_,signalName,dt,clearSignals=clearSignals,\
                                          orderType=1,price=price,**kwargs)

        return clearLongOrderRes

    @classmethod
    def clearShortWithNdang(cls, symbol_, vol_, signalName, dt, clearSignals=['allShort'], pattern='ACTIVE1',
                            **kwargs):

        if pattern == 'ACTIVE1':
            price = getHQ_dangwei(dt, symbol_, 'sell', 0)
        if pattern == 'POSITIVE1':
            price = getHQ_dangwei(dt, symbol_, 'buy', 0)

        clearShortOrderRes = cls.clearShort(symbol_, vol_, signalName, dt, clearSignals=clearSignals, \
                                          orderType=1, price=price, **kwargs)
        return clearShortOrderRes

    def fengexian(self):
        i=1

    @classmethod
    def cancelOpenLong(cls,context,symbol,dt,orderLog):
        return  cancelOrder(context,symbol,1,1,dt,orderLog=orderLog)


    @classmethod
    def cancelOpenShort(cls,context,symbol,dt,orderLog):
        return cancelOrder(context,symbol,2,1,dt,orderLog=orderLog)

    @classmethod
    def cancelClearLong(cls, context,symbol,dt,orderLog):
        return cancelOrder(context,symbol, 2, 2,dt,orderLog=orderLog)

    @classmethod
    def cancelClearShort(cls, context,symbol,dt,orderLog):
        return cancelOrder(context,symbol, 1, 2,dt,orderLog=orderLog)

    @classmethod
    def cancelAllOrder(cls,dt,**kwargs):

        waitOrderS = get_unfinished_orders()
        for aOrder in waitOrderS:
            orderDict = {}

            orderDict['cl_ord_id'] = aOrder.cl_ord_id
            orderDict['account_id'] = aOrder.account_id
            order_cancel(orderDict)

            # if positionEffect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:
            #     if side==1:
            #         pside=2
            #     if side==2:
            #         pside=1
            #     waitAvailPosition(context,symbol_,pside)
            orderLog = kwargs.get('orderLog', None)
            if orderLog is not None:
                sigMsg = 'cancel order'
                symbol_=aOrder.symbol
                side=aOrder.side
                positionEffect=aOrder.position_effect
                # cls.orderLog.info("%s,%s,%d,%d,%d,%s",dt, symbol_,vol_,OrderSide_Buy,PositionEffect_Open,signalName)
                # cls.orderLog.info("%s,%s,%s", dt, symbol_,sigMsg+'-'+symbol_)
                orderLog.info("%s,%s,%s", dt, symbol_,
                              sigMsg + '-' + symbol_ + '-' + str(side) + '-' + str(positionEffect))



    def writeOrderToFile(self,side_,position_effect_,filename='order.txt'):

        """ 装饰器 """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                """ A wrapper function """

                symbol_=args[0]
                vol_=args[1]
                signalName_=args[2]

                if side_==OrderSide_Buy:
                    strSide='buy'
                if side_==OrderSide_Sell:
                    strSide='sell'
                if position_effect_==PositionEffect_Open:
                    strPosEffect='open'
                if position_effect_==PositionEffect_Close:
                    strPosEffect='close'


                msg = "%s,%s,%s,%s,%s"%(symbol_,str(vol_),strSide,strPosEffect,signalName_)
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                pathAndName =current_date+'-'+filename
                f = open(pathAndName, 'a')  # 若是'wb'就表示写二进制文件
                f.write(msg)
                f.close()



                res = func(*args, **kwargs)
                return res
            return wrapper
        return decorator





def getMainContractData_Fade(continuousContract,sDatetime,eDatetime):
    #sDatetime 可以是日期带时间，也可以仅仅是日期

    dateList=commonHelpBylw.splitDates(sDatetime,eDatetime)
    dfMainContract = pd.DataFrame(columns=['mainContract', 'symbol', 'datetime'])
    index_ = 0
    for aContinu in continuousContract:
        for sDtime_,eDtime_ in dateList:
            tempMainContract=get_continuous_contracts(csymbol=aContinu, \
                                                  start_date=sDtime_, end_date=eDtime_)

            for atem in tempMainContract:
                dfMainContract.loc[index_, 'mainContract'] = aContinu
                dfMainContract.loc[index_, 'symbol'] = atem['symbol']
                dfMainContract.loc[index_, 'datetime'] = atem['trade_date']
                index_ = index_ + 1
            i=1
    


    dfMainContract['datetime']=dfMainContract['datetime'].dt.strftime('%Y-%m-%d')
    mainContractData = dfMainContract.pivot(index='datetime', columns='mainContract', values='symbol')

    return mainContractData

def getMainSymbolLastFinishTradingDate(underlySyms,lastDate):
    #lastDate 表示当前时刻，已经走完了的交易日。具体来源于calendar模块中 get_latest_finished_tradingdate函数
#underlySyms 必须是list
    #返回值也是一个list
    mainContractData = getMainContractData_Fade(underlySyms, lastDate, lastDate)
    if not mainContractData.empty:
        currNeedMainSymbol = mainContractData.to_numpy()[0].tolist()
        return currNeedMainSymbol


def getMulData(contractList,mulSDate,muleDate):
    mulDict={}
    for aContract in contractList:
        aMul = get_history_instruments(aContract, fields=None, \
                                       start_date=mulSDate, end_date=muleDate)
        symbolCode = aContract

        if len(aMul) == 0:
            print(aContract, ' has no mul from juejin')
            mulDict[symbolCode] = 1
            continue
        aMul = aMul[0]

        mulValue = aMul['multiplier']
        mulDict[symbolCode] = mulValue
    return mulDict


def getSlippageRatio(underLyingSymList):

    asym = getMainSymbolLastFinishTradingDate(underLyingSymList, '2020-03-04')
    ratioList=[]
    for acontract in asym:
        ticks = getCurrentTick('2020-03-04 09:30:30', acontract)
        danghq_1 = ticks[0]
        buyPrice = danghq_1['bid_p']
        sellPrice = danghq_1['ask_p']
        spreadPrice = sellPrice - buyPrice


        # 计算合约价值占比

        ratio_ = 10000.0 * spreadPrice / (buyPrice)
        ratioList.append((acontract,ratio_))
    return pd.DataFrame.from_records(ratioList,columns=['symbol','slipRatio'])

def getHQData_Fade(symbolist,sDateTime,eDateTim,fre='60s',fields_='symbol,eob,open,high,low,close',adjust=1,adjust_end_time=''):
    # dateList = commonHelpBylw.splitDates(sDateTime, eDateTim)
    # dfData = pd.DataFrame()
    #
    # for symbol_ in symbolist:
    #     for sDtime_, eDtime_ in dateList:
    #         tempHQdata = history(symbol=symbol_,frequency=fre,start_time=sDtime_,end_time=eDtime_,fields=fields_,df=True)
    #
    #         dfData=dfData.append(tempHQdata)
    #
    # return dfData



    #上面由于splitDates无法对于分钟线日期准确的拆分。所以上面这种方式取数据不太对
    #下面用新逻辑。
    # 先取全部数据，然后查看刚出来数据的最后一个日期，取他的下一个秒时间。一直循环到最后取不出来数据为止。
    # sDtime_=sDateTime
    # eDtime_=eDateTim

    if fre=='tick':
        dateName='created_at'
    else:
        dateName='eob'


    dfData = pd.DataFrame()
    for symbol_ in symbolist:
        sDtime_ = sDateTime
        eDtime_ = eDateTim
        tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_, \
                             fields=fields_, df=True,adjust=adjust,adjust_end_time=adjust_end_time)

        while not tempHQdata.empty:
            tempHQdata = tempHQdata.sort_values(dateName)
            dfData = dfData.append(tempHQdata)
            latestDateTime=tempHQdata[dateName].iloc[-1]

            nextDT=latestDateTime+Second()
            sDtime_=nextDT.strftime('%Y-%m-%d %H:%M:%S')
            if sDtime_<=eDtime_:
                tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_,
                                     fields=fields_, df=True,adjust=adjust)
            else:
                #即下一个初始时间大于了最终结束时间，说明数据已经取完了。
                break
    return dfData


def downDoadData(symbolist,sDateTime,eDateTim,filename,fre='60s',fields_='symbol,eob,open,high,low,close',adjust=1,adjust_end_time=''):
    import os
    if fre == 'tick':
        dateName = 'created_at'
    else:
        dateName = 'eob'


    for symbol_ in symbolist:
        sDtime_ = sDateTime
        eDtime_ = eDateTim
        tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_, \
                             fields=fields_, df=True, adjust=adjust, adjust_end_time=adjust_end_time)

        columns=list(tempHQdata.columns)
        while not tempHQdata.empty:
            tempHQdata = tempHQdata[columns]
            tempHQdata = tempHQdata.sort_values(dateName)

            if os.path.exists(filename):
                tempHQdata.to_csv(filename, mode='a', header=False, index=False)
            else:
                tempHQdata.to_csv(filename, mode='a', header=True, index=False)


            # dfData = dfData.append(tempHQdata)
            latestDateTime = tempHQdata[dateName].iloc[-1]

            nextDT = latestDateTime + Second()
            sDtime_ = nextDT.strftime('%Y-%m-%d %H:%M:%S')
            if sDtime_ <= eDtime_:
                tempHQdata = history(symbol=symbol_, frequency=fre, start_time=sDtime_, end_time=eDtime_,
                                     fields=fields_, df=True, adjust=adjust)


            else:
                # 即下一个初始时间大于了最终结束时间，说明数据已经取完了。
                break


#direction 表示是 方向，是买的档位还是卖的档位
#dangweiNum表示档位 0 表示 买卖一档，1表示买卖2档，2表示买卖的第3档等等。
#f返回结果是-888 表示 该档位的价格不存在，可能是涨停，或者跌停了。
def getHQ_dangwei(dt,symbol_,direction,dangweiNum):
    sdt = dt
    import datetime
    datetime.datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S")
    edt = datetime.datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
    sdt=edt-datetime.timedelta(minutes=30)
    sdt=sdt.strftime("%Y-%m-%d %H:%M:%S")
    edt = edt.strftime("%Y-%m-%d %H:%M:%S")
    tickHq = getHQData_Fade([symbol_], sdt, edt, fre='tick',
                            fields_='symbol,created_at,open,high,low,quotes')

    # dangHQ是一个list，第0个元素是买卖一档，第一个元素是买卖二挡
    dangHQ = tickHq['quotes'].iloc[-1]

    danghq_1 = dangHQ[dangweiNum]
    if direction=='buy':

        if 'bid_p' not in danghq_1 or danghq_1['bid_v']==0:
            return -888
        return danghq_1['bid_p']  # 平多的对手价，平多是卖，那么对手价肯定是买档位的价格。



    if direction=='sell':
        if 'ask_p' not in danghq_1 or  danghq_1['ask_v']==0:
            return -888
        return danghq_1['ask_p']  # 平多的我方价格，平多是卖，那么我方价肯定是卖档位的价格。


def getCurrentTick(dt,symbol_):
    sdt = dt
    import datetime
    datetime.datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S")
    edt = datetime.datetime.strptime(sdt, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
    sdt=edt-datetime.timedelta(minutes=30)
    sdt=sdt.strftime("%Y-%m-%d %H:%M:%S")
    edt = edt.strftime("%Y-%m-%d %H:%M:%S")
    tickHq = getHQData_Fade([symbol_], sdt, edt, fre='tick',
                            fields_='symbol,created_at,open,high,low,quotes')

    # dangHQ是一个list，第0个元素是买卖一档，第一个元素是买卖二挡
    dangHQ = tickHq['quotes'].iloc[-1]

    return dangHQ


#获取主力连续的数据。不是简单的标的资产，而是每个具体时间，都是具体的合约代码

def getHQDataOfMainContract_Fade(underlyingSymbolList,sDateTime,eDateTim,fre='60s',fields_='symbol,eob,open,high,low,close'):

    #1 先获取主力连续行情表，只带上了标的资产的id，
    #2、将具体时间 计算出其所属的交易日
    #3、取出标的资产的主力连续表
    #4、主力连续表和主力连续行情表，以交易日 做连接

    hqDF=getHQData_Fade(underlyingSymbolList,sDateTime,eDateTim,fre=fre,fields_=fields_)

    aNewTradeCalendar = calendayBylw.getACalendarInstance()
    hqDF['eob']=hqDF['eob'].dt.strftime("%Y-%m-%d %H:%M:%S")
    hqDF['tradeDate']=hqDF['eob'].apply(aNewTradeCalendar.tradeDateTimeTradingDateOffset,aoffset=0)

    mainContractDf=getMainContractData_Fade(underlyingSymbolList,sDateTime,eDateTim)
    mainContractDfAdjust=mainContractDf.stack().reset_index(name='symbol')

    mergeDf=pd.merge(hqDF,mainContractDfAdjust,left_on=['tradeDate','symbol'],right_on=['datetime','mainContract'])

    resulDf=mergeDf.copy()

    resulDf.rename(index=str,columns={"symbol_y": "symbol"},inplace=True)

    strList=fields_.split(',')
    resulDf=resulDf[strList]

    resulDf['eob'] = pd.to_datetime(resulDf['eob'], format="%Y-%m-%d %H:%M:%S")
    resulDf['eob'] = resulDf['eob'].dt.tz_localize(tz=timezone(timedelta(hours=8)))

    

    return resulDf


def getInstumInfo(symbols,fields='symbol,exchange,sec_id,listed_date,delisted_date'):
    #symbols 是list

    instuInfo=get_instruments(symbols=symbols, fields=fields, df=True)
    return instuInfo




def dealwithGmTradeRecord(f):
    #f是交易明细被打开后的，类似这种f = open('交易明细.csv',encoding="gbk")
    realTradeData = pd.read_csv(f, header=0, index_col=False)

    # realTradeData=pd.read_csv('a.csv',encoding="gbk",index_col=False)
    # realTradeData=pd.read_csv('aa1.csv')
    # realTradeData=pd.read_csv('aa.csv')

    realTradeData.columns = realTradeData.columns.str.strip()

    # tradeRecordDf=realTradeData[['exchange','side','symbol','positionEffect','filledVolume','filledVwap','createdAt','filledCommission']]
    # tradeRecordDf.columns=['secName','direction','symbol','PositionEffect','volume','tradePrice','tradeDateTime','commission']
    #

    tradeRecordDf = realTradeData[
        ['side', 'symbol', 'positionEffect', 'filledVolume', 'filledVwap', 'createdAt', 'filledCommission']]
    tradeRecordDf.columns = ['direction', 'symbol', 'PositionEffect', 'volume', 'tradePrice', 'tradeDateTime',
                             'commission']
    tradeRecordDf = tradeRecordDf.dropna()

    tradeRecordDf['tradeDateTime'] = pd.to_datetime(tradeRecordDf['tradeDateTime'], format='%Y-%m-%dT%H:%M:%SZ')
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.tz_localize(tz=timezone.utc)
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.tz_convert(tz=timezone(timedelta(hours=8)))
    tradeRecordDf['tradeDateTime'] = tradeRecordDf['tradeDateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    tradeRecordDf = tradeRecordDf.sort_values('tradeDateTime', kind='mergesort')

    tradeRecordDf = tradeRecordDf.replace(
        {'direction': {1: '买', 2: '卖'}, 'PositionEffect': {1: '开仓', 2: '平仓', 3: '平今仓', 4: '平昨仓'}})
    # ss=inputDF['direction'].map({1:'买',2:'卖'})

    return tradeRecordDf
    # tradeRecordDf.to_csv('gmTradeRecord.csv', index=False, encoding='gbk')


def waitAvailPosition(context,symbol_,posiSide=PositionSide_Long):


    while(1):
        symbolHolding = context.account().position(symbol=symbol_, side=posiSide)
        if symbolHolding and symbolHolding['available'] > 0:
            break
        else:
            print('cancle order wait position %s,%d'%(symbol_,posiSide),' ',symbolHolding)
            time.sleep(0.5)


def cancelOrder(context,symbol_,side,positionEffect,dt,**kwargs):

    waitOrderS=get_unfinished_orders()
    for aOrder in waitOrderS:
        orderDict={}
        if aOrder.symbol==symbol_ and \
            aOrder.side==side and \
                ((positionEffect==2 and aOrder.position_effect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]) or \
                        positionEffect==aOrder.position_effect):
            orderDict['cl_ord_id']=aOrder.cl_ord_id
            orderDict['account_id'] = aOrder.account_id
            order_cancel(orderDict)

            # if positionEffect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:
            #     if side==1:
            #         pside=2
            #     if side==2:
            #         pside=1
            #     waitAvailPosition(context,symbol_,pside)
            orderLog = kwargs.get('orderLog', None)
            if orderLog is not None:

                sigMsg='cancel order'
                # cls.orderLog.info("%s,%s,%d,%d,%d,%s",dt, symbol_,vol_,OrderSide_Buy,PositionEffect_Open,signalName)
                # cls.orderLog.info("%s,%s,%s", dt, symbol_,sigMsg+'-'+symbol_)
                orderLog.info("%s,%s,%s", dt, symbol_, sigMsg + '-' + symbol_ + '-' + str(side)+ '-' + str(positionEffect))

            return True
        else:
            return False




#下委托价的时候，委托价 要符合交易所规定的跳数，否则实盘会报废单。这个掘金的模拟盘没有这个报错，导致我模拟盘的时候没有测试出来
def getAdjustLimitPrice(initLimitPrice,symbol,direction):
    adf=getInstumInfo([symbol],fields='symbol,price_tick')
    priceTick=adf['price_tick'].iloc[0]

    mul=initLimitPrice//priceTick
    if initLimitPrice%priceTick!=0:
        if direction==1:
            adjustPrice=mul*priceTick+priceTick
        if direction==-1:
            adjustPrice = (mul-1) * priceTick + priceTick
        return adjustPrice
    else:
        return initLimitPrice
    i=1


def gmPositionToMongoPosition(allpositions,monPositions):
    # allpositions = context.account().positions()
    hol=[]
    for apo in allpositions:
        tempdict={}
        tempdict['_id']=apo['symbol']+'_'+str(apo['side'])
        tempdict['vwap'] =apo['vwap']
        tempdict['vol'] = apo['volume']
        tempdict['created_at'] = apo['created_at']
        tempdict['updated_at'] = apo['updated_at']
        tempdict['available'] = apo['available']
        hol.append(tempdict)
    # import pymongo
    # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    # db = client['simulate_short_period']
    # acollection = db['holding']
    monPositions.addPositions(hol)


def gmPositionToDf(context):

    allpositions = context.account().positions()

    cashobj=context.account().cash
    hol=[]
    for apo in allpositions:
        tempdict={}

        tempdict['symbol'] = apo['symbol']
        tempdict['side'] = str(apo['side'])
        tempdict['vwap'] =apo['vwap']
        tempdict['vol'] = apo['volume']
        tempdict['nav']=cashobj['nav']
        hol.append(tempdict)
    df = pd.DataFrame.from_records(hol)
    return df


#主要用来处理，委托回报全部成交后，等待持仓到位
def isPositionsFilledByOrder(context,gmorder):
    import time
    symbol_ = gmorder.symbol
    positionSide_ = gmorder.side
    cusposi = context.account().position(symbol_, positionSide_)

    while (1):
        # 即能够查到的持仓，刚好是这个委托全部成交的持仓
        if cusposi is not None and cusposi.volume >= gmorder.volume:
            return True
        else:
            print(cusposi,' ',gmorder.volume)
            time.sleep(1)





# # 切换到 commonhelp
# def getSymboInfoDataFromGm(aGmAPIfun,symbolList,sDateTime,eDateTime,fields=None,step_=3000):
# # def getSymboInfoDataFromGm(symbolList,sDateTime,eDateTime,fields=None,step_=3000):
#
#     #aGmAPIfun 是掘金的提取数据的函数，可以是history，也可以是get_history_instruments，等等。反正是一次提取历史数据
#     #不能太长的话，都可以用这里的这个函数包一层。
#
#
#     #准备一个 日历对象。
#     currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     currDate = currDateTime[0:10]
#     nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
#                       + DateOffset(years=1)
#     nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
#     aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
#     aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)
#
#
#
#     #起始日期 和 结束日期 分别往前 和 往后扩展一下。
#     sDate=sDateTime[0:10]
#     eDate=eDateTime[0:10]
#
#     ssDate=aNewTradeCalendar.mDatesOffset(sDate,doffset=-1,leftOrright=-1)
#     eeDate = aNewTradeCalendar.mDatesOffset(eDate, doffset=1, leftOrright=1)
#
#
#     atradeDateSerial=aNewTradeCalendar.getADateTimeSeries(ssDate,eeDate)
#
#
#
#     dfInfo=pd.DataFrame()
#     for aSymbol in symbolList:
#         sIndex=0
#         eIndex=sIndex+step_-1
#         while True:
#             cSdate=atradeDateSerial.iloc[sIndex]
#             if eIndex>=atradeDateSerial.shape[0]:
#                 cEdate=atradeDateSerial.iloc[-1]
#             else:
#                 cEdate=atradeDateSerial.iloc[eIndex]
#
#             # tempInfoDf=get_history_instruments(aSymbol, fields=fields, start_date=cSdate, \
#             #                         end_date=cEdate, df=True)
#             tempInfoDf = aGmAPIfun(aSymbol, fields=fields, start_date=cSdate, \
#                                                  end_date=cEdate, df=True)
#
#             dfInfo=dfInfo.append(tempInfoDf)
#
#             if eIndex>=atradeDateSerial.shape[0]:
#                 break
#             else:
#                 sIndex = sIndex+step_
#                 eIndex = eIndex + step_
#     return dfInfo
#






