import xlrd
import os
import sys

class PBNormalAttackRootSheetData:
    def __init__(self, idColumnIndex):
        self.idColumnIndex = idColumnIndex
        self.dict = self.PBNormalAttackRootCollect(self.idColumnIndex)

    def PBNormalAttackRootCollect(self, idColumnIndex):
        data = xlrd.open_workbook("E:\TestTools\getSheetData\conf\excel\attack.xlsx")
        table = data.sheet_by_name("PBNormalAttackRoot")
        rowNum = table.nrows
        colNum = table.ncols
        sourceHeadList = table.row_values(0)
        sourceIDList = []
        headList = []
        for i in sourceHeadList:
            if i != "":
                headList.append(i)
        for i in range(rowNum):
            sourceIDList.append(table.row_values(i)[idColumnIndex])
        firstDict = {}
        secondDict = {}
        for i in range(rowNum):
            for j in range(colNum):
                secondDict[sourceHeadList[j]] = table.cell(i, j).value
            firstDict[sourceIDList[i]] = secondDict
            secondDict = {}  # reset secondDict
        return (firstDict)

    def getValueByID(self, key, columnname):
        return self.dict[key][columnname]