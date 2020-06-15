# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:13:59 2018

@author: lw
"""



class HoldingPostions():
    
    
    def __init__(self,symbol_,positionSide_,volume_,strategyOrderId_=None):

        self.__strategyOrderId=strategyOrderId_
        self.__symbol=symbol_
        self.__positionSide=positionSide_
        self.__volume=volume_

    @property
    def symbol(self):
        return self.__symbol

    @property
    def positionSide(self):
        return self.__positionSide

    @property
    def volume(self):
        return self.__volume



