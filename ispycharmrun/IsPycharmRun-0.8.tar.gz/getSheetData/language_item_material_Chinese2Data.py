import xlrd
import os
import sys

class material_Chinese2SheetData:
    def __init__(self, idColumnIndex):
        self.idColumnIndex = idColumnIndex
        self.dict = self.material_Chinese2Collect(self.idColumnIndex - 1)

    def material_Chinese2Collect(self, idColumnIndex):
        data = xlrd.open_workbook(r"/Users/shiboxuan/testTools/getSheetData/conf/excel/Language/language_item.xlsx")
        table = data.sheet_by_name("material_Chinese2")
        rowNum = table.nrows
        colNum = table.ncols
        sourceHeadList = table.row_values(0)
        sourceIDList = []
        headList = []
        for i in sourceHeadList:
            if i != "":
                headList.append(i)
        for i in range(rowNum):
            value = table.row_values(i)[idColumnIndex]
            if type(value) == float:
                if value == int(value):
                    value = int(value)
            sourceIDList.append(str(value))
        firstDict = {}
        secondDict = {}
        for i in range(rowNum):
            for j in range(colNum):
                value = table.cell(i, j).value
                if type(value) == float:
                    if value == int(value):
                        value = int(value)
                secondDict[sourceHeadList[j]] = str(value)
            firstDict[sourceIDList[i]] = secondDict
            secondDict = {}  # reset secondDict
        return (firstDict)

    def getValueByID(self, key, columnname):
        return self.dict[key][columnname]

    def getMainKeyList(self):
        list = []
        for i in self.dict.keys():
            try:
                int(i)
                list.append(i)
            except ValueError:
                continue
        return list