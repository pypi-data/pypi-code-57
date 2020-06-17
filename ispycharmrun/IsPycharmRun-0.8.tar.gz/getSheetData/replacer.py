import os
import xlrd
import sys
import platform


class replacer:
    def __init__(self):
        self.workPath = self.getWorkPath()
        print(self.workPath)
        self.excelPath = self.workPath + os.sep + "conf" + os.sep + "excel"
        self.pathList = self.traverseFile()
        print(self.pathList)
        self.relationDict = self.getSheetRelation()
        print("init success")

    def getWorkPath(self):
        workPath = os.path.dirname(__file__)
        print(workPath)
        return workPath.replace("/", os.sep)

    def traverseFile(self):
        pathList = []
        for root, _, files in os.walk(self.excelPath):
            for file in files:
                if os.path.splitext(file)[1] == ".xlsx":
                    pathList.append(root + os.sep + file)
        return pathList

    def getSheetRelation(self):
        relationDict = {}
        for i in self.pathList:
            #filename = i.split(".")[0].split("\\")[-1]
            realSheetList = []
            file = xlrd.open_workbook(i)
            sheetList = file.sheet_names()
            for j in sheetList:
                if "#" not in j:
                    realSheetList.append(j)
                    #print(j)
            if  not realSheetList:
                continue
            relationDict[i] = realSheetList
        #print(relationDict)
        return relationDict

    def replaceSheetData(self):
        for key in self.relationDict:
            for j in self.relationDict[key]:
                #j = j.encode('utf-8')
                #print(key)
                if platform.system() == "Windows":
                    os.system("copy sheetDataStruct.py %s_%sData.py"%(str(key.split(".")[0].split(os.sep)[-1]), str(j)))
                elif platform.system() == "Darwin":
                    os.system("cp sheetDataStruct.py %s_%sData.py"%(str(key.split(".")[0].split(os.sep)[-1]), str(j)))
                print("%s_%sData.py"%(str(key.split(".")[0].split(os.sep)[-1]), str(j)))
                file = open("%s_%sData.py"%(str(key.split(".")[0].split(os.sep)[-1]),j))
                tempStr = file.read()
                file.close()
                temp = tempStr.replace("xxx", str(j))
                strFile = temp.replace("yyy", key)
                # strFile = strFile.replace("\\", "/")

                with open("%s_%sData.py"%(str(key.split(".")[0].split(os.sep)[-1]),str(j)), "w") as f:
                    f.write(strFile)

    def _isContainsChinese(self,testStr):
        for char in testStr:
            if '\u4e00' <= char <= '\u9fa5':
                return True
        return False

if __name__ == "__main__":
    a = replacer()
    #print a.workPath
    #print a.excelPath
    #print a.pathList
    #a.getSheetRelation()
    a.replaceSheetData()
