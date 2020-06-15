# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 21:34:13 2018

@author: SH
"""


# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
import numpy as np
import pandas as pd


from pyalgotrade import gm3HelpBylw
from pyalgotrade import commonHelpBylw


try:
    import talib
except:
    print('请安装TA-Lib库')
from gm.api import *
import datetime


class tradeRecordObj():
    #加一列mul。
    
    
    #合约的合约乘数发现，并不是一个时间序列，而是每个具体合约 合约乘数是固定的。可能同一个品种的不同合约会
    #合约乘数不一样，但是同一个合约的合约乘数绝对是同一个值。
    
    
    def __addMul(self):
        self.jiaogeDf['mul']=1
        if self.mulDf.empty:
            return
        
        for i in range(self.jiaogeDf.shape[0]):
            sym=self.jiaogeDf['symbol'].iloc[i]
            date=self.jiaogeDf['tradeDate'].iloc[i]
            self.jiaogeDf['mul'].iloc[i]=self.mulDf.loc[date,sym]
            
   #交割单字段只能是如下
   #['tradeDate','tradeDateTime','symbol','direction','PositionEffect','tradePrice','volume','commission']
    def __init__(self,aDf,aCusCalendar,aMul=pd.DataFrame(),aMulDict={}):
        aDf=aDf.sort_values(by=['tradeDateTime'],kind='mergesort')
        self.jiaogeDf=aDf
#        self.mulDf=aMul
#        self.__addMul()
        
        self.mulDict=aMulDict
        
        
        self.clearName=['平仓','平今仓','平昨仓','平今','平昨']
        self.aCusCalendar=aCusCalendar
        
        
        self.__clearedTradeRecordDf=self.__productTradeMatchDf()
        self.clearedDFwithProfit = self.getAOpenClearPairProfit()
        
        
        print('*****')
        
        
        i=1
    
    
    def __productTradeMatchDf(self):

        
        
        tradeMatchDf=self.jiaogeDf.groupby('symbol').apply(self.__tradeMatch)
        tradeMatchDf=tradeMatchDf.sort_values(by=['cleartradeDateTime'])
        tradeMatchDf.index=tradeMatchDf.index.droplevel(1)
        tradeMatchDf=tradeMatchDf.reset_index()
        
        return tradeMatchDf

    
        #期货在计算的时候要
    def __tradeMatch(self,aGroup):
        
       
        openLongDf=aGroup.loc[(aGroup['direction']=='买')&(aGroup['PositionEffect']=='开仓')] 
        clearLongDf=aGroup.loc[(aGroup['direction']=='卖')&\
                       ( aGroup['PositionEffect'].isin(self.clearName) )]

        openShortDf=aGroup.loc[(aGroup['direction']=='卖')&(aGroup['PositionEffect']=='开仓')]
        clearShortDf=aGroup.loc[(aGroup['direction']=='买')&\
                       ( aGroup['PositionEffect'].isin(self.clearName) )]
        
        resDF=pd.DataFrame()
        resIn=0
        
        
        #多头头寸的处理
#        
        
        def merge2DF(openLongDf,clearLongDf):
            
        
            if not openLongDf.empty and not clearLongDf.empty:
#                openLongDf=openLongDf.sort_values(by=['tradeDate','tradeTime'])
#                clearLongDf=clearLongDf.sort_values(by=['tradeDate','tradeTime'])
                i=1
                
            resDF=pd.DataFrame()
            resIn=0
            openin=0
            clearin=0
            
            
            while openin<openLongDf.shape[0] and clearin<clearLongDf.shape[0]:
                
                
                
                # longOpenDT=openLongDf['tradeDate'].iloc[openin]+' '+openLongDf['tradeTime'].iloc[openin]
                # longClearDT=clearLongDf['tradeDate'].iloc[clearin]+' '+clearLongDf['tradeTime'].iloc[clearin]

                longOpenDT = openLongDf['tradeDateTime'].iloc[openin]
                longClearDT = clearLongDf['tradeDateTime'].iloc[clearin]


                
                if longOpenDT<=longClearDT:
                    resDF.loc[resIn,'opentradeDateTime']=openLongDf['tradeDateTime'].iloc[openin]
                    # resDF.loc[resIn,'opentradeTime']=openLongDf['tradeTime'].iloc[openin]
                    
                    resDF.loc[resIn,'cleartradeDateTime']=clearLongDf['tradeDateTime'].iloc[clearin]
                    # resDF.loc[resIn,'cleartradeTime']=clearLongDf['tradeTime'].iloc[clearin]
       
                    resDF.loc[resIn,'openTradePrice']=openLongDf['tradePrice'].iloc[openin]
                    resDF.loc[resIn,'clearTradePrice']=clearLongDf['tradePrice'].iloc[clearin]
    
#                    resDF.loc[resIn,'openMul']=openLongDf['mul'].iloc[openin]
#                    resDF.loc[resIn,'clearMul']=clearLongDf['mul'].iloc[clearin]
                    

                
                    
                    if clearLongDf['volume'].iloc[clearin]<openLongDf['volume'].iloc[openin]:
                        # 手续费 要看拆出来多少份，又因为的开平仓对，只是挑出了其中的部分手数。
                        resDF.loc[resIn, 'clearCom'] = clearLongDf['commission'].iloc[clearin]
                        resDF.loc[resIn, 'openCom'] = (openLongDf['commission'].iloc[openin] /
                                                       openLongDf['volume'].iloc[openin]) \
                                                      * clearLongDf['volume'].iloc[clearin]
                        openLongDf['commission'].iloc[openin] = openLongDf['commission'].iloc[openin] - resDF.loc[
                            resIn, 'openCom']

                        resDF.loc[resIn,'vol']=clearLongDf['volume'].iloc[clearin]
  
                        openLongDf['volume'].iloc[openin]=openLongDf['volume'].iloc[openin]-\
                        clearLongDf['volume'].iloc[clearin]




                        clearin=clearin+1
                        resIn=resIn+1
                        continue
                        
                        
                        
                    if clearLongDf['volume'].iloc[clearin]==openLongDf['volume'].iloc[openin]:
                        
                        
                        resDF.loc[resIn,'vol']=openLongDf['volume'].iloc[openin]
                        resDF.loc[resIn, 'clearCom'] = clearLongDf['commission'].iloc[clearin]
                        resDF.loc[resIn, 'openCom'] = openLongDf['commission'].iloc[openin]



                        openin=openin+1
                        clearin=clearin+1
                        resIn=resIn+1
                        continue
                        
                    if clearLongDf['volume'].iloc[clearin]>openLongDf['volume'].iloc[openin]:

                        resDF.loc[resIn, 'openCom'] = openLongDf['commission'].iloc[openin]
                        resDF.loc[resIn, 'clearCom'] = (clearLongDf['commission'].iloc[clearin] /
                                                        clearLongDf['volume'].iloc[clearin]) \
                                                       * openLongDf['volume'].iloc[openin]
                        clearLongDf['commission'].iloc[clearin] = clearLongDf['commission'].iloc[clearin] - resDF.loc[
                            resIn, 'clearCom']


                        resDF.loc[resIn,'vol']=openLongDf['volume'].iloc[openin]

                        clearLongDf['volume'].iloc[clearin]=-openLongDf['volume'].iloc[openin]+\
                        clearLongDf['volume'].iloc[clearin]





                        
                        openin=openin+1
                        resIn=resIn+1
                        continue
                    
                    #else 这里的情况是，开仓时间大于了 平仓时间
                    #认定 这笔平仓，没有对应的开仓记录，略过。
                else:
                    resDF.loc[resIn,'opentradeDateTime']=np.nan
                    # resDF.loc[resIn,'opentradeTime']=np.nan
                    
                    resDF.loc[resIn,'cleartradeDateTime']=clearLongDf['tradeDateTime'].iloc[clearin]
                    # resDF.loc[resIn,'cleartradeTime']=clearLongDf['tradeTime'].iloc[clearin]
                    
                  
                    
                    resDF.loc[resIn,'openTradePrice']=np.nan
                    resDF.loc[resIn,'clearTradePrice']=clearLongDf['tradePrice'].iloc[clearin]     
                    
#                    resDF.loc[resIn,'openMul']=np.nan
#                    resDF.loc[resIn,'clearMul']=clearLongDf['mul'].iloc[clearin]
#                    
                    resDF.loc[resIn,'openCom']=np.nan
                    resDF.loc[resIn,'clearCom']=clearLongDf['commission'].iloc[clearin]
                    
                    resDF.loc[resIn,'vol']=clearLongDf['volume'].iloc[clearin]
                    clearin=clearin+1
                    resIn=resIn+1
                    continue
            
            #归并排序算法中，对跳出循环的一只进行处理
            if openin==openLongDf.shape[0] and clearin<clearLongDf.shape[0]:
                while clearin<clearLongDf.shape[0]:
                    
                    resDF.loc[resIn,'opentradeDateTime']=np.nan
                    # resDF.loc[resIn,'opentradeTime']=np.nan
                    
                    resDF.loc[resIn,'cleartradeDateTime']=clearLongDf['tradeDateTime'].iloc[clearin]
                    # resDF.loc[resIn,'cleartradeTime']=clearLongDf['tradeTime'].iloc[clearin]
                    
                  
                    
                    resDF.loc[resIn,'openTradePrice']=np.nan
                    resDF.loc[resIn,'clearTradePrice']=clearLongDf['tradePrice'].iloc[clearin]     
                    
#                    resDF.loc[resIn,'openMul']=np.nan
#                    resDF.loc[resIn,'clearMul']=clearLongDf['mul'].iloc[clearin]
                    
                    resDF.loc[resIn,'openCom']=np.nan
                    resDF.loc[resIn,'clearCom']=clearLongDf['commission'].iloc[clearin]
                    
                    resDF.loc[resIn,'vol']=clearLongDf['volume'].iloc[clearin]
                    clearin=clearin+1
                    resIn=resIn+1
                    continue
                
            if openin<openLongDf.shape[0] and clearin==clearLongDf.shape[0]:
                while openin<openLongDf.shape[0]:
                    
                    resDF.loc[resIn,'cleartradeDateTime']=np.nan
                    # resDF.loc[resIn,'cleartradeTime']=np.nan
                    
                    resDF.loc[resIn,'opentradeDateTime']=openLongDf['tradeDateTime'].iloc[openin]
                    # resDF.loc[resIn,'opentradeTime']=openLongDf['tradeTime'].iloc[openin]
                    
                  
                    
                    resDF.loc[resIn,'clearTradePrice']=np.nan
                    resDF.loc[resIn,'openTradePrice']=openLongDf['tradePrice'].iloc[openin]     
                    
#                    resDF.loc[resIn,'clearMul']=np.nan
#                    resDF.loc[resIn,'openMul']=openLongDf['mul'].iloc[openin]
                    
                    resDF.loc[resIn,'clearCom']=np.nan
                    resDF.loc[resIn,'openCom']=openLongDf['commission'].iloc[openin]
                    
                    resDF.loc[resIn,'vol']=openLongDf['volume'].iloc[openin]
                    openin=openin+1
                    resIn=resIn+1
                    continue
        
            return resDF
        

                 
                    
                    
                    
        longRes=merge2DF(openLongDf,clearLongDf)            
        longRes['positionSide']='long'
        
        shortRes=merge2DF(openShortDf,clearShortDf)            
        shortRes['positionSide']='short'
        
        resDF=longRes.append(shortRes)
        return resDF
    


    def __openClearMatchNoDTime(self,aGroup):
        openLongDf=aGroup.loc[(aGroup['direction']=='买')&(aGroup['PositionEffect']=='开仓')]
        clearLongDf=aGroup.loc[(aGroup['direction']=='卖')&\
                       (aGroup['PositionEffect'].isin(self.clearName))]

        openShortDf=aGroup.loc[(aGroup['direction']=='卖')&(aGroup['PositionEffect']=='开仓')]
        clearShortDf=aGroup.loc[(aGroup['direction']=='买')&\
                       (aGroup['PositionEffect'].isin(self.clearName))]
        
        resDF=pd.DataFrame()
        resIn=0
        
        
        #多头头寸的处理
#        
        
        def merge2DF(openLongDf,clearLongDf):
            
        
            if not openLongDf.empty and not clearLongDf.empty:
                openLongDf=openLongDf.sort_values(by=['tradeDate','tradeTime'])
                clearLongDf=clearLongDf.sort_values(by=['tradeDate','tradeTime'])
                
            resDF=pd.DataFrame()
            resIn=0
            openin=0
            clearin=0
            
           
            
            while openin<openLongDf.shape[0] and clearin<clearLongDf.shape[0]:  
                resDF.loc[resIn,'opentradeDate']=openLongDf['tradeDate'].iloc[openin]
                resDF.loc[resIn,'opentradeTime']=openLongDf['tradeTime'].iloc[openin]
                
                resDF.loc[resIn,'cleartradeDate']=clearLongDf['tradeDate'].iloc[clearin]
                resDF.loc[resIn,'cleartradeTime']=clearLongDf['tradeTime'].iloc[clearin]
   
                resDF.loc[resIn,'openTradePrice']=openLongDf['tradePrice'].iloc[openin]
                resDF.loc[resIn,'clearTradePrice']=clearLongDf['tradePrice'].iloc[clearin]

                resDF.loc[resIn,'openMul']=openLongDf['mul'].iloc[openin]
                resDF.loc[resIn,'clearMul']=clearLongDf['mul'].iloc[clearin]
                
                resDF.loc[resIn,'openCom']=openLongDf['commission'].iloc[openin]
                resDF.loc[resIn,'clearCom']=clearLongDf['commission'].iloc[clearin]
            
                
                if clearLongDf['volume'].iloc[clearin]<openLongDf['volume'].iloc[openin]:
                    
    
                    resDF.loc[resIn,'vol']=clearLongDf['volume'].iloc[clearin]
  
                    openLongDf['volume'].iloc[openin]=openLongDf['volume'].iloc[openin]-\
                    clearLongDf['volume'].iloc[clearin]
                    
                    clearin=clearin+1
                    resIn=resIn+1
                    continue
                    
                    
                    
                if clearLongDf['volume'].iloc[clearin]==openLongDf['volume'].iloc[openin]:
                    
                    
                    resDF.loc[resIn,'vol']=openLongDf['volume'].iloc[openin]
  
                    openin=openin+1
                    clearin=clearin+1
                    resIn=resIn+1
                    continue
                    
                if clearLongDf['volume'].iloc[clearin]>openLongDf['volume'].iloc[openin]:
                    
    
                    resDF.loc[resIn,'vol']=openLongDf['volume'].iloc[openin]
    
                    
                   
                    
                    clearLongDf['volume'].iloc[clearin]=-openLongDf['volume'].iloc[openin]+\
                    clearLongDf['volume'].iloc[clearin]
                    
                    openin=openin+1
                    resIn=resIn+1
                    continue
            
        
            return resDF
        longRes=merge2DF(openLongDf,clearLongDf)            
        longRes['positionSide']='long'
        
        shortRes=merge2DF(openShortDf,clearShortDf)            
        shortRes['positionSide']='short'
        
        resDF=longRes.append(shortRes)
        return resDF

    
    
    
    def getTradeStatistics(self):
        """
        仿照 文华财经的输出报告。输出交易统计。具体格式见笔记

    直接忽略了没有平仓的东东。即只算了 开平仓对的收益。如果有未平仓的情况，忽略了。具体间笔记“统计交易次数”
    
        """
        
        
        #求交易次数。认为两笔交易，开仓日期时间相同，平仓日期时间也相同，认为该两笔交易是同一笔。
        def tradeCount(aGroup):
            if aGroup['symbol'].iloc[0]=='CFFEX.IF1812':
                ii=1
            
            dropDul=aGroup.drop_duplicates(subset=['opentradeDateTime','cleartradeDateTime'],\
                                           keep='first', inplace=False)
            
            count=dropDul.shape[0]
            return count
        
        #求交易次数。认为两笔交易，开仓日期相同，平仓日期也相同，认为该两笔交易是同一笔。
        def tradeCountNoTime(aGroup):
            
            dropDul=aGroup.drop_duplicates(subset=['opentradeDate','cleartradeDate'],\
                                           keep='first', inplace=False)
            
            count=dropDul.shape[0]
            return count
        
        #这个求交易次数是 按照开平仓记录表，有几条记录就算几次，不按照时间来统计。
        #文华财经就是按照这种方法统计的。
        def tradeCountOrginal(aGroup):
            count=aGroup.shape[0]
            return count
        
        
        countDf=self.__clearedTradeRecordDf.groupby(by=['symbol','positionSide'])\
            .apply(tradeCount)
        
        
        
        
        #下面是算每个品种的收益。手数
        
        # def addAProfit(aSeries):
        #     if aSeries['positionSide']=='long':
        #         return (-aSeries['openTradePrice']+aSeries['clearTradePrice'])\
        #                     *aSeries['vol']*self.mulDict[aSeries['symbol']]\
        #                 -aSeries['openCom']-aSeries['clearCom']
        #
        #     else:
        #         return (aSeries['openTradePrice']-aSeries['clearTradePrice'])\
        #                     *aSeries['vol']*self.mulDict[aSeries['symbol']]\
        #                 -aSeries['openCom']-aSeries['clearCom']
        #
        #
        # clearedDFwithProfit=self.__clearedTradeRecordDf.copy()
        # clearedDFwithProfit['profit']=clearedDFwithProfit.apply(addAProfit,axis=1)
        #

        
        profitOfevryContDf=self.clearedDFwithProfit.groupby(by=['symbol','positionSide'])\
                            [['profit','vol']].sum()
        
        profitOfevryContDf['tradeCount']=countDf
        
        profitOfevryContDf=profitOfevryContDf.reset_index()
        
        return profitOfevryContDf
        


    #一个 开平仓 对的 收益
    def getAOpenClearPairProfit(self):
        # 下面是算每个品种的收益。手数

        def addAProfit(aSeries):
            if aSeries['positionSide'] == 'long':
                return (-aSeries['openTradePrice'] + aSeries['clearTradePrice']) \
                       * aSeries['vol'] * self.mulDict[aSeries['symbol']] \
                       - aSeries['openCom'] - aSeries['clearCom']

            else:
                return (aSeries['openTradePrice'] - aSeries['clearTradePrice']) \
                       * aSeries['vol'] * self.mulDict[aSeries['symbol']] \
                       - aSeries['openCom'] - aSeries['clearCom']

        clearedDFwithProfit = self.__clearedTradeRecordDf.copy()
        clearedDFwithProfit['profit'] = clearedDFwithProfit.apply(addAProfit, axis=1)
        return clearedDFwithProfit

    
    
    #日内收益 交易收益 持仓收益中的  日内收益实现
    def intradayProfit(self):
        
        
        dataDf=self.jiaogeDf
     
    
        reDf=dataDf.groupby(by=['tradeDate','symbol']).apply(self.__openClearMatchNoDTime)  
        reDf.index=reDf.index.droplevel(2)
        
        
        def afun(adf):
            if adf['positionSide']=='long':
                profit=-adf['openTradePrice']*adf['vol']*adf['openMul']\
                        +adf['clearTradePrice']*adf['vol']*adf['clearMul']\
                        -adf['openCom']-adf['clearCom']
            
            if adf['positionSide']=='short':
                profit=adf['openTradePrice']*adf['vol']*adf['openMul']\
                        -adf['clearTradePrice']*adf['vol']*adf['clearMul']\
                        -adf['openCom']-adf['clearCom']
            return profit
        
        
        reDf['profit']=reDf.apply(afun,axis=1)
        return reDf
    
    #计算日内开平记录的成交额
    def intradayAmount(self):
        dataDf=self.jiaogeDf
     
    
        reDf=dataDf.groupby(by=['tradeDate','symbol']).apply(self.__openClearMatchNoDTime)  
        reDf['amount']=reDf['clearMul']*reDf['clearTradePrice']*reDf['vol']+\
                        reDf['openMul']*reDf['openTradePrice']*reDf['vol']
        reDf.index=reDf.index.droplevel(2)
        i=1
        return reDf['amount'].sum()
        
   
 
    # 交易收益。按照定义是 有交易的时刻，比如开仓，平仓动作，交易的价格 比如开仓价格，平仓价格
#相对 该日的 收盘价而言，是赚了还是亏了多少前。比如多头开仓20，但是收盘价是40，也就是我这个开仓动作
#相对收盘，赚了20    
    def tradeProfitVSClose(self,closeData):
        dataDf=self.jiaogeDf
        
        
        
        def afun(aSeries):

            symbol=aSeries['symbol']
            close=closeData.loc[aSeries['tradeDate'],symbol]
            
#            if aSeries['direction']=='买' and aSeries['PositionEffect']=='开仓':
#                profit=(close-aSeries['tradePrice'])*1*1*\
#                                                aSeries['mul']*aSeries['volume']
#            if aSeries['direction']=='买' and (aSeries['PositionEffect'] in self.clearName):
#                profit=(close-aSeries['tradePrice'])*1*(-1)*\
#                                                aSeries['mul']*aSeries['volume']
#            if aSeries['direction']=='卖' and aSeries['PositionEffect']=='开仓':
#                profit=(close-aSeries['tradePrice'])*(-1)*(1)*\
#                                                aSeries['mul']*aSeries['volume']
#            if aSeries['direction']=='卖' and (aSeries['PositionEffect'] in self.clearName):
#                profit=(close-aSeries['tradePrice'])*(-1)*(-1)*\
#                                                aSeries['mul']*aSeries['volume']
#                                                
                                                
                                                
           #上面逻辑有问题。不要分开仓还是平仓，因为动作只有买和卖，不管是开仓还是平仓，动作是一样的
#那么买的动作就是 买的价格越低越好，卖的动作就是卖的价格越高越好
           
           #交易持仓要扣除手续费
            if aSeries['direction']=='买' :
                profit=(close-aSeries['tradePrice'])*1*\
                                                self.mulDict[symbol]*aSeries['volume']-aSeries['commission']
           
            if aSeries['direction']=='卖':
                profit=(close-aSeries['tradePrice'])*(-1)*\
                                                self.mulDict[symbol]*aSeries['volume']-aSeries['commission']
                                               
 
            return profit                                    
        dataDf['tradeProfit'] =dataDf.apply(afun,axis=1)
        tradeProDF=dataDf.groupby(by=['tradeDate','symbol'])['tradeProfit'].agg(sum)
        tradeProDF = tradeProDF.reset_index()
        # #下面 是将上面dataDf 合并开仓和平仓。
        #
        # longBoolindex=((dataDf['direction']=='买')&(dataDf['PositionEffect']=='开仓')) |\
        #                     ((dataDf['direction']=='卖')&(dataDf['PositionEffect'].isin(self.clearName)))
        # shortBoolindex=((dataDf['direction']=='卖')&(dataDf['PositionEffect']=='开仓')) |\
        #                     ((dataDf['direction']=='买')&(dataDf['PositionEffect'].isin(self.clearName)))
        #
        # tradeProfitDFNoKP=dataDf.copy()
        # tradeProfitDFNoKP['positionSi']=''
        # tradeProfitDFNoKP.loc[longBoolindex,'positionSi']='long'
        # tradeProfitDFNoKP.loc[shortBoolindex,'positionSi']='short'
        # tradeProDF=tradeProfitDFNoKP.groupby(by=['tradeDate','symbol','positionSi'])['tradeProfit'].agg(sum)
        # tradeProDF=tradeProDF.reset_index()


        return tradeProDF


 #交易收益扣除 日内
     #两个df分别通过intradayProfit和tradeProfitVSClose 来生成
    def tradeProfitNoIntra(self,tradeDF,intraDf):
        
        
        #思路是 日内的和交易收益 都按照 日期，品种，持仓方向  来列出来。然后一一对应相减。
        
        adjustIntraDF=intraDf.reset_index()
        adjustIntraDF=adjustIntraDF[['tradeDate','symbol','positionSide','profit']]
        adjustIntraDF=adjustIntraDF.groupby(by=['tradeDate','symbol','positionSide'])['profit'].agg(sum)
        adjustIntraDF=adjustIntraDF.reset_index()
        adjustIntraDF['profit'].sum()
        #交易收益表 做外连接。这样保证
        #交易收益表记录 都能够保存下来。
        mergeResu=pd.merge(adjustIntraDF,tradeDF,left_on=['tradeDate','symbol','positionSide'],\
                           right_on=['tradeDate','symbol','positionSi'],how='outer')
        
        
        mergeResu=mergeResu.fillna(0)
        mergeResu['dailyPro']=mergeResu['tradeProfit']-mergeResu['profit']
        
        return mergeResu
    
        
  
    
    
    def getTradeMatchDf(self):


        
        return self.__clearedTradeRecordDf
        
    


# 通过对于某个交易日cDate，找交割单中的记录，如果看cDate 落在开仓时间 和平仓时间之间来获取每日持仓
        #方法在笔记中讨论过了。这个函数没啥用。放着吧
    def positionEveryDaySave(self,dateSerial):

        positionDF=pd.DataFrame()
        
        tradeMatchDf=self.jiaogeDf.groupby('symbol').apply(self.__tradeMatch)
        tradeMatchDf=tradeMatchDf.sort_values(by=['opentradeDate'])
        tradeMatchDf.index=tradeMatchDf.index.droplevel(1)
        tradeMatchDf=tradeMatchDf.reset_index()
        
        tradeMatchDf=tradeMatchDf[tradeMatchDf['opentradeDate']!=tradeMatchDf['cleartradeDate']]
        for aDate in dateSerial.__iter__():
            aSelectDf=tradeMatchDf.loc[(tradeMatchDf['opentradeDate']<=aDate)&\
                                       (tradeMatchDf['cleartradeDate']>aDate)]
            aSelectDf=aSelectDf[['symbol','positionSide','opentradeDate','cleartradeDate','openTradePrice','vol']]
            aSelectDf['tradeDate']=aDate
            positionDF=positionDF.append(aSelectDf)
        
        positionDF=positionDF.drop(['cleartradeDate'], axis=1)
        positionDF=positionDF.groupby(by=['symbol','positionSide','tradeDate','openTradePrice'])['vol'].agg(sum)
        
        positionDF=positionDF.reset_index()
        return positionDF
    

    # #每日净持仓。即通过一个交易记录，或者是交割单记录。见笔记说明
    # def netPositionEveryDay(self):
    #     dataDf=self.jiaogeDf
    #
    #
    #     reDf=dataDf.groupby(by=['tradeDate','symbol']).apply(self.__openClearMatchNoDTime)
    #     reDf.index=reDf.index.droplevel(2)
    #
    #
    #     def afun(adf):
    #         if adf['positionSide']=='long':
    #             profit=-adf['openTradePrice']*adf['vol']*adf['openMul']\
    #                     +adf['clearTradePrice']*adf['vol']*adf['clearMul']\
    #                     -adf['openCom']-adf['clearCom']
    #
    #         if adf['positionSide']=='short':
    #             profit=adf['openTradePrice']*adf['vol']*adf['openMul']\
    #                     -adf['clearTradePrice']*adf['vol']*adf['clearMul']\
    #                     -adf['openCom']-adf['clearCom']
    #         return profit
    #
    #
    #     reDf['profit']=reDf.apply(afun,axis=1)
    #     return reDf
    
    
    
    #获取每个交易日的持仓情况.
    #按照交割单的   起始时间，结束时间 时间范围内的交易日 来求取每日持仓


    #这个看着是每日持仓,当时如果某个交易日,各个品种的持仓都是0的话,那么这个交易日都不会出现在表中的

    #finalPostionDF 是初始状态下，经过交割单一系列操作后，最后交易日，你拿到的持仓。也就是根据这个持仓
    #再加上过去的交割单，你可以反推出，过去每个交易日的持仓。
    def purePositionEveryDay(self,finalPostionDF):
        
        
        aSDate=self.jiaogeDf['tradeDate'].iloc[0]
        aEDate=self.jiaogeDf['tradeDate'].iloc[-1]
        aPreDate=self.aCusCalendar.tradingDaysOffset(aSDate,-1)


        #这个地方,日期还是只能用aCusCalendar来获取,不能根据交割单中的日期,因为
        #如果某几天完全没有交易,但是这几天还是可以有持仓的.如果用交割单中的日期,可能导致
        #这几日的持仓都没有显示出来.
        if finalPostionDF.empty:
            dateSeriesEndDate = aEDate
        else:

            dateSeriesEndDate = self.aCusCalendar.tradingDaysOffset(finalPostionDF['tradeDate'].iloc[0], -1)
        dateSerial = self.aCusCalendar.getADateTimeSeries(aPreDate, dateSeriesEndDate)

        dateSerial=dateSerial.sort_values(ascending=False)
        positionEveryDayDf=finalPostionDF.copy()
        

        dateSerialLen=len(dateSerial)
        
        positionColumnsName=list(finalPostionDF.columns.values)
        for poNum in range(dateSerialLen):
            
            aDate=dateSerial.iloc[poNum]

            # if aDate=='2019-12-04':
            #     i=1
            aTime='00:00:00'
            if aDate in positionEveryDayDf['tradeDate'].values:
                continue
            else:
                
                
                #当前日期的下一个交易日，这样来获取下一个交易日的持仓，然后下一个交易日的交易记录。
                #然后两者相减，得到本交易日的持仓
                if poNum>=1:
                    nextDate=dateSerial.iloc[poNum-1]
                else:
                    nextDate = self.aCusCalendar.tradingDaysOffset(aDate,1)
                
                nextDayPostionDf=positionEveryDayDf.loc[positionEveryDayDf['tradeDate']==nextDate]
                nextDayTradeDf=self.jiaogeDf.loc[self.jiaogeDf['tradeDate']==nextDate]
                
                
                
                # aSelectDf=nextDayPostionDf.copy()
                
                #将时间从下一个交易日，变换为当前交易日
                nextDayPostionDf['tradeDate']=aDate
                
                #如果没有交易记录，那么当前的持仓，就是 未来的下一个交易日的持仓拷贝过来
                if nextDayTradeDf.empty: 
                    
                    positionEveryDayDf=positionEveryDayDf.append(nextDayPostionDf)
                else:
                    
                    #下一个交易日的交易记录拿出来后。希望从后往前考察它。
                    reversnextDayTradeDf=nextDayTradeDf[::-1]
                    for row_number,row in reversnextDayTradeDf.iterrows():
                        
                        
                            
                        sym=row['symbol']
                        dire=row['direction']
                        positionEffect=row['PositionEffect']
                        vol=row['volume']
                        tradePirce=row['tradePrice']
                        
                        # if aDate=='2018-08-24' and sym=='CZCE.MA901':
                        #     i=1
                        #
                        
                        #判断出当前交易是对多头持仓有影响的交易
                        if (dire == '买' and positionEffect == '开仓')or(dire=='卖' and (positionEffect in self.clearName)):
                            longBoolindex=(nextDayPostionDf['symbol']==sym)&\
                                                         (nextDayPostionDf['positionSide']=='long')
                        if dire=='买' and positionEffect=='开仓':
                            aSeriesPos=nextDayPostionDf.loc[longBoolindex]
                            
                            if aSeriesPos.empty:
                                aTuple=(sym,'long',-vol,tradePirce,aDate)
                                aPositDF=pd.DataFrame.from_records([aTuple],columns=positionColumnsName)
                                nextDayPostionDf=nextDayPostionDf.append(aPositDF)
                            else:
                                nextDayPostionDf.loc[longBoolindex,'vol']=nextDayPostionDf.loc[longBoolindex,'vol']-vol
                            
                        if dire=='卖' and (positionEffect in self.clearName):
                            
                            
                            aLongPosition=nextDayPostionDf.loc[longBoolindex]
                            
                            #如果是未来持仓中没有该标的的情况
                            if aLongPosition.empty:
                                aTuple=(sym,'long',vol,tradePirce,aDate)
                                aPositDF=pd.DataFrame.from_records([aTuple],columns=positionColumnsName)
                                nextDayPostionDf=nextDayPostionDf.append(aPositDF)
                                
                                #如果是未来持仓中有该标的的情况
                            else:
                                nextDayPostionDf.loc[longBoolindex,'vol']=nextDayPostionDf.loc[longBoolindex,'vol']+vol
                                
                                
                        #判断出当前交易是对空头有影响的交易
                        if (dire=='卖' and positionEffect=='开仓') or (
                                dire=='买' and (positionEffect in self.clearName)):
                            shortBoolindex=(nextDayPostionDf['symbol']==sym)&\
                                                         (nextDayPostionDf['positionSide']=='short')
                        if dire=='卖' and positionEffect=='开仓':
                            aSeriesPos=nextDayPostionDf.loc[shortBoolindex]
                            
                            if aSeriesPos.empty:
                                aTuple=(sym,'short',-vol,tradePirce,aDate)
                                aPositDF=pd.DataFrame.from_records([aTuple],columns=positionColumnsName)
                                nextDayPostionDf=nextDayPostionDf.append(aPositDF)
                            else:
                                
                                nextDayPostionDf.loc[shortBoolindex,'vol']=nextDayPostionDf.loc[shortBoolindex,'vol']-vol
                            
                            
                        if dire=='买' and (positionEffect in self.clearName):
                            
                            
                            aSeriesPos=nextDayPostionDf.loc[shortBoolindex]
                            
                            #如果是未来持仓中没有该标的的情况
                            if aSeriesPos.empty:
                                aTuple=(sym,'short',vol,tradePirce,aDate)
                                aPositDF=pd.DataFrame.from_records([aTuple],columns=positionColumnsName)
                                nextDayPostionDf=nextDayPostionDf.append(aPositDF)
                                
                                #如果是未来持仓中有该标的的情况
                            else:
                                nextDayPostionDf.loc[shortBoolindex,'vol']=nextDayPostionDf.loc[shortBoolindex,'vol']+vol




                    #如果是下一个交易日某个品种有持仓,但是改品种 下一个交易日没有交易记录,则说明本交易日改品种的持仓
                    #和下一个交易日的这个持仓一样.下面两句代码 能够考虑这个情况.
                    nextDayPostionDf=nextDayPostionDf.loc[nextDayPostionDf['vol']!=0]
                    positionEveryDayDf=positionEveryDayDf.append(nextDayPostionDf)
        return positionEveryDayDf

        # 每日持仓。用向量化的方式重写.上面方式数据多了,循环 会慢.
        # 按照交割单的   起始时间，结束时间 时间范围内的交易日 来求取每日持仓
    #finalPositionDf ['symbol','positionSide','vol','cost','tradeDate']

    #算了.先放着.感觉逻辑也不好理.等到上面函数实在不行了.就来改吧.
    def purePositionEveryDay_vecotr(self, finalPostionDF):

        aSDate = self.jiaogeDf['tradeDate'].iloc[0]
        aEDate = self.jiaogeDf['tradeDate'].iloc[-1]
        aPreDate = self.aCusCalendar.tradingDaysOffset(aSDate, -1)

        if finalPostionDF.empty:
            dateSeriesEndDate=aEDate
        else:

            dateSeriesEndDate=aCusCalendar.tradingDaysOffset(finalPostionDF['tradeDate'].iloc[0], -1)
        dateSerial = self.aCusCalendar.getADateTimeSeries(aPreDate, dateSeriesEndDate)

        dateDf=dateSerial.to_frame()

        # dateSerial = dateSerial.sort_values(ascending=False)

        # def amergeFun(aGroup):
        #     singleSymbolJiaoGeEveryTradingDays=pd.merge(aGroup,dateDf,left_on='tradeDa')
        # self.jiaogeDf.groupby('symbol').apply(pd.merge,left)

        # self.jiaogeDf

        positionEveryDayDf = finalPostionDF.copy()





        dateSerialLen = len(dateSerial)

        positionColumnsName = list(finalPostionDF.columns.values)
        for poNum in range(dateSerialLen):

            aDate = dateSerial.iloc[poNum]

            aTime = '00:00:00'
            if aDate in positionEveryDayDf['tradeDate'].values:
                continue
            else:

                # 当前日期的下一个交易日，这样来获取下一个交易日的持仓，然后下一个交易日的交易记录。
                # 然后两者相减，得到本交易日的持仓
                if poNum >= 1:
                    nextDate = dateSerial.iloc[poNum - 1]
                else:
                    nextDate = self.aCusCalendar.tradingDaysOffset(aDate, 1)

                nextDayPostionDf = positionEveryDayDf.loc[positionEveryDayDf['tradeDate'] == nextDate]
                nextDayTradeDf = self.jiaogeDf.loc[self.jiaogeDf['tradeDate'] == nextDate]

                # aSelectDf=nextDayPostionDf.copy()

                # 将时间从下一个交易日，变换为当前交易日
                nextDayPostionDf['tradeDate'] = aDate

                # 如果没有交易记录，那么当前的持仓，就是 未来的下一个交易日的持仓拷贝过来
                if nextDayTradeDf.empty:

                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)
                else:

                    # 下一个交易日的交易记录拿出来后。希望从后往前考察它。
                    reversnextDayTradeDf = nextDayTradeDf[::-1]
                    for row_number, row in reversnextDayTradeDf.iterrows():

                        sym = row['symbol']
                        dire = row['direction']
                        positionEffect = row['PositionEffect']
                        vol = row['volume']
                        tradePirce = row['tradePrice']

                        # if aDate=='2018-08-24' and sym=='CZCE.MA901':
                        #     i=1
                        #

                        # 判断出当前交易是对多头持仓有影响的交易
                        if (dire == '买' and positionEffect == '开仓') or (
                                dire == '卖' and (positionEffect in self.clearName)):
                            longBoolindex = (nextDayPostionDf['symbol'] == sym) & \
                                            (nextDayPostionDf['positionSide'] == 'long')
                        if dire == '买' and positionEffect == '开仓':
                            aSeriesPos = nextDayPostionDf.loc[longBoolindex]

                            if aSeriesPos.empty:
                                aTuple = (sym, 'long', -vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                            else:
                                nextDayPostionDf.loc[longBoolindex, 'vol'] = nextDayPostionDf.loc[
                                                                                 longBoolindex, 'vol'] - vol

                        if dire == '卖' and (positionEffect in self.clearName):

                            aLongPosition = nextDayPostionDf.loc[longBoolindex]

                            # 如果是未来持仓中没有该标的的情况
                            if aLongPosition.empty:
                                aTuple = (sym, 'long', vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)

                                # 如果是未来持仓中有该标的的情况
                            else:
                                nextDayPostionDf.loc[longBoolindex, 'vol'] = nextDayPostionDf.loc[
                                                                                 longBoolindex, 'vol'] + vol

                        # 判断出当前交易是对空头有影响的交易
                        if (dire == '卖' and positionEffect == '开仓') or (
                                dire == '买' and (positionEffect in self.clearName)):
                            shortBoolindex = (nextDayPostionDf['symbol'] == sym) & \
                                             (nextDayPostionDf['positionSide'] == 'short')
                        if dire == '卖' and positionEffect == '开仓':
                            aSeriesPos = nextDayPostionDf.loc[shortBoolindex]

                            if aSeriesPos.empty:
                                aTuple = (sym, 'short', -vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)
                            else:

                                nextDayPostionDf.loc[shortBoolindex, 'vol'] = nextDayPostionDf.loc[
                                                                                  shortBoolindex, 'vol'] - vol

                        if dire == '买' and (positionEffect in self.clearName):

                            aSeriesPos = nextDayPostionDf.loc[shortBoolindex]

                            # 如果是未来持仓中没有该标的的情况
                            if aSeriesPos.empty:
                                aTuple = (sym, 'short', vol, tradePirce, aDate)
                                aPositDF = pd.DataFrame.from_records([aTuple], columns=positionColumnsName)
                                nextDayPostionDf = nextDayPostionDf.append(aPositDF)

                                # 如果是未来持仓中有该标的的情况
                            else:
                                nextDayPostionDf.loc[shortBoolindex, 'vol'] = nextDayPostionDf.loc[
                                                                                  shortBoolindex, 'vol'] + vol

                    # 如果是下一个交易日某个品种有持仓,但是改品种 下一个交易日没有交易记录,则说明本交易日改品种的持仓
                    # 和下一个交易日的这个持仓一样.下面两句代码 能够考虑这个情况.
                    nextDayPostionDf = nextDayPostionDf.loc[nextDayPostionDf['vol'] != 0]
                    positionEveryDayDf = positionEveryDayDf.append(nextDayPostionDf)
        return positionEveryDayDf

    #持仓收益。注意，当日的持仓，是拿来算下一个交易日的持仓收益的。上一交易日的持仓，是用来算
    #本交易日的持仓收益的
    def positionProfit(self,positionEveryDayDf,closeData):
        
        maxDate=positionEveryDayDf['tradeDate'].max()
        
        def afun(aRow):
            sym=aRow['symbol']
            date=aRow['tradeDate']
            
            
            close=closeData.loc[date,sym]
            
            symData=closeData[sym].dropna()
            preClose=symData.loc[symData.index<date].iloc[-1]
            
            if np.isnan(close) or np.isnan(preClose):
                print('close is nan')
            
            aRow['close']=close
            aRow['preClose']=preClose
            aRow['mul']=self.mulDict[sym]
            
            if aRow['positionSide']=='long':
                
                aRow['profit']=(aRow['close']-aRow['preClose'])*aRow['mul']*aRow['vol']*(1)
            if aRow['positionSide']=='short':
                
                aRow['profit']=(aRow['close']-aRow['preClose'])*aRow['mul']*aRow['vol']*(-1)
            return aRow
        
        yesDayPositionDf=positionEveryDayDf.copy()
        yesDayPositionDf['tradeDate']=yesDayPositionDf['tradeDate'].apply(self.aCusCalendar.tradingDaysOffset,args=(1,))
        
        
        # maxDate=yesDayPositionDf['tradeDate'].max()
        # yesDayPositionDf=yesDayPositionDf.loc[yesDayPositionDf['tradeDate']<maxDate]

        cmpDate=closeData.index[-1]
        yesDayPositionDf=yesDayPositionDf.loc[yesDayPositionDf['tradeDate']<=cmpDate]
        adjustPoProfitDF=yesDayPositionDf.apply(afun,axis=1)
        return adjustPoProfitDF
    
        
    #生成每个品种的,每日收益序列
    def profitEveryTDay(self,finalPostionDF,symbolflag='underlyingSymbol'):

        #finalPostionDF=pd.DataFrame(columns=['symbol','positionSide','vol','cost','tradeDate']) 可以只是这么一个空的dataframe
        #symbolflag='underlyingSymbol' 表示具体的合约要合并成 品种.

        #finalPostionDF中 成本价 只能是成交价格的平均，不能包含手续费，tradeDate 是交易日，用来记录是哪天的持仓，字符串。
        #positionSide 只能是long和short 的字符串

        currNeedContract = self.jiaogeDf['symbol'].drop_duplicates().values
        tradeSDate = self.jiaogeDf['tradeDate'].iloc[0]
        tradeDate = self.jiaogeDf['tradeDate'].iloc[-1]

        # 起始日期多给 一天
        hSDate = self.aCusCalendar.tradingDaysOffset(tradeSDate, -1)
        hqdata=gm3HelpBylw.getHQData_Fade(currNeedContract,hSDate,tradeDate,fre='1d',fields_='symbol,eob,close')

        hqdata['eob']=hqdata['eob'].dt.strftime('%Y-%m-%d %H:%M:%S')
        hqdata['eob']=hqdata['eob'].str[0:10]
        closeData = hqdata.pivot(index='eob', columns='symbol', values='close')



        #************************持仓收益********************

        # finalPostionDF = pd.DataFrame(columns=['symbol', 'positionSide', 'vol', 'cost', 'tradeDate'])
        positionDf=self.purePositionEveryDay(finalPostionDF)
        if not positionDf.empty:
            positionProfitDf=self.positionProfit(positionDf,closeData)
        else:
            positionProfitDf=pd.DataFrame(columns=['symbol', 'positionSide', 'vol', 'cost', 'tradeDate','profit'])



        #多个合约的持仓收益,合并到一个品种.这种情况下,持仓的成本,量,是没法合并的,因为合约不同
        #两个cost 怎么合并.
        #所以只需要保存一个持仓收益.
        if symbolflag == 'underlyingSymbol':
            positionProfitDf['underLyingSym']=positionProfitDf['symbol'].apply((commonHelpBylw.getMainContinContract))
            # underLyingSymPositionProfit=positionProfitDf.groupby(by=['underLyingSym','tradeDate'])['profit'].apply(sum)
            positionProfitDf = positionProfitDf.groupby(by=['underLyingSym', 'tradeDate'])['profit'].apply(
                sum)
            positionProfitDf = positionProfitDf.reset_index()
            positionProfitDf = positionProfitDf.rename(columns={'underLyingSym': 'symbol'})




        # ************************交易收益********************
        #下面处理交易收益

        tradeProfit=self.tradeProfitVSClose(closeData)

        if symbolflag=='underlyingSymbol':
            tradeProfit['underLyingSym']=tradeProfit['symbol'].apply((commonHelpBylw.getMainContinContract))
            tradeProfit=tradeProfit.groupby(by=['underLyingSym', 'tradeDate'])['tradeProfit'].apply(sum)
            tradeProfit=tradeProfit.reset_index()
            tradeProfit = tradeProfit.rename(columns={'underLyingSym': 'symbol'})




        #合并成一个每日收益
        # if positionDf.empty:
        #     profitEveryTDayDf=tradeProfit.copy()
        #     profitEveryTDayDf=profitEveryTDayDf.rename(columns={'tradeProfit':'profit'})
        #
        #     profitEveryTDayDf=profitEveryTDayDf.pivot(index='tradeDate',columns='underLyingSym',values='profit')
        #
        #     aDateDf=self.aCusCalendar.getADateTimeSeries(hSDate,tradeDate).to_frame()
        #
        #     #连接,补充完整交易日
        #     adf=pd.merge(profitEveryTDayDf,aDateDf,how='right',left_index=True,right_on='tradingDays')
        #     adf=adf.fillna(0)
        #     adf=adf.reset_index(drop=True)
        #
        #     return adf

        profitEveryTDayDf = tradeProfit.copy()
        profitEveryTDayDf = profitEveryTDayDf.rename(columns={'tradeProfit': 'profit'})

        profitEveryTDayDf = profitEveryTDayDf.pivot(index='tradeDate', columns='symbol', values='profit')

        aDateDf = self.aCusCalendar.getADateTimeSeries(hSDate, tradeDate).to_frame()

        # 连接,补充完整交易日
        adf = pd.merge(profitEveryTDayDf, aDateDf, how='right', left_index=True, right_on='tradingDays')
        adf = adf.fillna(0)
        adf = adf.reset_index(drop=True)



        #将持仓收益加进来
        for ainx,arow in positionProfitDf.iterrows():
            sym=arow['symbol']
            dt=arow['tradeDate']
            profit=arow['profit']

            adf.loc[adf['tradingDays']==dt,sym]=adf.loc[adf['tradingDays']==dt,sym]+profit
        return adf


    def netAssetValueTDay(self,finalPostionDF,iniCash):
        profitEveryDayDf=self.profitEveryTDay(finalPostionDF)
        colNameList=list(profitEveryDayDf.columns)
        colNameList.remove('tradingDays')

        netprofitEDay = profitEveryDayDf.copy()
        netprofitEDay['allprofit'] = 0
        for aCname in colNameList:
            netprofitEDay['allprofit'] = netprofitEDay['allprofit'] + netprofitEDay[aCname]

        netprofitEDay['NetAssetValue'] = netprofitEDay['allprofit']
        netprofitEDay['NetAssetValue'].iloc[0] = iniCash
        netprofitEDay['NetAssetValue'] = netprofitEDay['NetAssetValue'].cumsum()

        return netprofitEDay






    #####下面处理夜盘函数

    #将品种中 有夜盘的品种 的交易额 统计出来。yepanDf 是具体的品种有无夜盘的表

    #逻辑就是，将交割单中的品种 全部变换成主力合约的名字，因为夜盘表 就是用主力合约标记的
    #然后将夜盘表 和交割单 连接起来。
    def yepanAmount(self,yepanDF):
        
        adjustJiaogedanDF=self.jiaogeDf.copy()
        adjustJiaogedanDF['mainContra']=adjustJiaogedanDF['symbol'].apply(commonHelpBylw.getMainContract)
        yepanMerge=pd.merge(yepanDF,adjustJiaogedanDF,left_on='symbol',right_on='mainContra',how='right')
        yepanMerge['amount']=yepanMerge['tradePrice']*yepanMerge['volume']*yepanMerge['mul']
        
        return yepanMerge


    #成交记录合并成一条。即认为成交时间在多少分钟之内，就认为同一个合约的同方向的成交 应该合并。
    def mergeTrades(self,seconds=60*30):
        adjustJiaogedanDF = self.jiaogeDf.copy()
        adjustJiaogedanDF['tradeDateTime']=pd.to_datetime(adjustJiaogedanDF['tradeDateTime'],format='%Y-%m-%d %H:%M:%S')

        def mergefun(adf):

            finanlDf=pd.DataFrame()


            nextDf=adf.copy()
            while not nextDf.empty:
                eDt = nextDf['tradeDateTime'].iloc[0] + datetime.timedelta(seconds=seconds)
                currDf=nextDf.loc[adf['tradeDateTime']<=eDt]
                nextDf=nextDf.loc[adf['tradeDateTime']>eDt]
                tempMergeDf=currDf.head(1)
                tempMergeDf['volume']=currDf['volume'].sum()
                tempMergeDf['commission'] = currDf['commission'].sum()
                finanlDf=finanlDf.append(tempMergeDf)

            return finanlDf





        ss=adjustJiaogedanDF.groupby(['symbol','direction','PositionEffect']).apply(mergefun)

        ss=ss.reset_index(drop=True)
        return ss