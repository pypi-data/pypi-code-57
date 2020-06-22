# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 22:09:40 2018

@author: SH
"""

import pandas as pd
import numpy as np



#获取平仓记录。即一条开仓记录，一条平仓记录 对应起来
def getCleardRecord(tradeRecordDF):
    
    #tradeRecordDF 这个df只能有 symbol，tradeDate,tradeTime,tradePrice,volumn
    #direction PositionEffect 这几个字段
    
    
    
    #加一个字段，将时间和日期写在一起，方便比较。
    tradeRecordDF['tTradeDateTime']=tradeRecordDF['tradeDate']+' '+tradeRecordDF['tradeTime']   
    agp=tradeRecordDF.groupby('symbol')
    
    
    
    def aSymbolFun(aGroup):
        
        if aGroup['symbol'].iloc[0]=='CZCE.TA905':
            iii=1
        def openClearMatch(openLongDf,clearLongDf,positionSideStr):
            
            cols=['positionSide','opentradeDate','opentradeTime','openTradePrice','cleartradeDate','cleartradeTime','clearTradePrice','vol']
            resDF=pd.DataFrame(columns=cols)
            resIn=0
            if not openLongDf.empty and not clearLongDf.empty:
                
                
                openLongDf=openLongDf.sort_values(by='tTradeDateTime')
                clearLongDf=clearLongDf.sort_values(by='tTradeDateTime')
                
                
                openin=0
                clearin=0
                
                
                while openin<openLongDf.shape[0] and clearin<clearLongDf.shape[0]:
                    
    #                resDF.loc[resIn,'positionSide']='long'
                    
                    
        #            resDF.loc[resIn,'openTradeAmount']=openLongDf['tradeAmount'].iloc[openin]
        #            resDF.loc[resIn,'clearTradeAmount']=clearLongDf['tradeAmount'].iloc[clearin]
                    
        #            resDF.loc[resIn,'mul']=clearLongDf['mul'].iloc[clearin]
                    
                    resDF.loc[resIn,'opentradeDate']=openLongDf['tradeDate'].iloc[openin]
                    resDF.loc[resIn,'opentradeTime']=openLongDf['tradeTime'].iloc[openin]
                        
                    resDF.loc[resIn,'cleartradeDate']=clearLongDf['tradeDate'].iloc[clearin]
                    resDF.loc[resIn,'cleartradeTime']=clearLongDf['tradeTime'].iloc[clearin]
  
                    resDF.loc[resIn,'openTradePrice']=openLongDf['tradePrice'].iloc[openin]
                    resDF.loc[resIn,'clearTradePrice']=clearLongDf['tradePrice'].iloc[clearin]
        
        
                    #匹配的时候开仓时间要保证晚于平仓时间
                    if openLongDf['tTradeDateTime'].iloc[openin]<clearLongDf['tTradeDateTime'].iloc[clearin]:
                        
                        
                    
                        if clearLongDf['volumn'].iloc[clearin]<openLongDf['volumn'].iloc[openin]:
                            
            
                            resDF.loc[resIn,'vol']=clearLongDf['volumn'].iloc[clearin]
            
                            
                            
                            
                            openLongDf['volumn'].iloc[openin]=openLongDf['volumn'].iloc[openin]-\
                            clearLongDf['volumn'].iloc[clearin]
                            
                            clearin=clearin+1
                            resIn=resIn+1
                            continue
                            
                            
                            
                        if clearLongDf['volumn'].iloc[clearin]==openLongDf['volumn'].iloc[openin]:
                            
                            
                            resDF.loc[resIn,'vol']=openLongDf['volumn'].iloc[openin]
                            
                            
                            
                            
                            openin=openin+1
                            clearin=clearin+1
                            resIn=resIn+1
                            continue
                            
                        if clearLongDf['volumn'].iloc[clearin]>openLongDf['volumn'].iloc[openin]:
                            
            
                            resDF.loc[resIn,'vol']=openLongDf['volumn'].iloc[openin]
            
                            
                           
                            
                            clearLongDf['volumn'].iloc[clearin]=-openLongDf['volumn'].iloc[openin]+\
                            clearLongDf['volumn'].iloc[clearin]
                            
                            openin=openin+1
                            resIn=resIn+1
                            continue
                    else:
                        resDF.loc[resIn,'vol']=openLongDf['volumn'].iloc[clearin]
                        resDF.loc[resIn,'opentradeDate']=np.nan
                        resDF.loc[resIn,'opentradeTime']=np.nan
                        resDF.loc[resIn,'openTradePrice']=np.nan
                        clearin=clearin+1
                        resIn=resIn+1
                        continue
                        
                    
            else:#if openLongDf.empty or clearLongDf.empty:
                if openLongDf.empty and not clearLongDf.empty:
                    
                    for rindex,row in clearLongDf.iterrows():
                        
                        resDF.loc[resIn,'cleartradeDate']=row['tradeDate']
                        resDF.loc[resIn,'cleartradeTime']=row['tradeTime']
                        resDF.loc[resIn,'clearTradePrice']=row['tradePrice']
                        resDF.loc[resIn,'vol']=row['volumn']
                    
                        resIn=resIn+1
                    
                    
                if not openLongDf.empty and  clearLongDf.empty:
                    
                    for rindex,row in openLongDf.iterrows():
                        resDF.loc[resIn,'opentradeDate']=row['tradeDate']
                        resDF.loc[resIn,'opentradeTime']=row['tradeTime']
                        resDF.loc[resIn,'openTradePrice']=row['tradePrice']
                        resDF.loc[resIn,'vol']=row['volumn']
                        
                        resIn=resIn+1
                    
            
    #        resDF.loc[resIn,'positionSide']='long'
            if resIn>=1:
                resDF['positionSide']=positionSideStr
            return resDF  
        
        
        
        
        openLongDf=aGroup.loc[(aGroup['direction']=='买')&(aGroup['PositionEffect']=='开仓')]
        clearLongDf=aGroup.loc[(aGroup['direction']=='卖')&\
                               ((aGroup['PositionEffect']=='平仓')|(aGroup['PositionEffect']=='平今'))]            
        resuLong=openClearMatch(openLongDf,clearLongDf,'long')  
    
    
        openShortDf=aGroup.loc[(aGroup['direction']=='卖')&(aGroup['PositionEffect']=='开仓')]
        clearShortDf=aGroup.loc[(aGroup['direction']=='买')&\
                               ((aGroup['PositionEffect']=='平仓')|(aGroup['PositionEffect']=='平今'))]      
        
        resuShort=openClearMatch(openShortDf,clearShortDf,'short')
        
        
        resul= resuLong.append(resuShort)     
        return resul      
    clearedTradeRecordDf=agp.apply(aSymbolFun)
    return clearedTradeRecordDf 
        
    
    