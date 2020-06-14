import xlrd
# import xlutils
from xlutils.copy import copy
import xlwt
import logging

_logger=logging.getLogger(__name__)
class ExcelUtil(object):
    # New File
    class NewExcelFile():
        def __init__(self, path, sheetName):
            '''

            :param path:保存路径
            :param sheetName: 表格名称
            '''
            self.path = path
            self.wb = xlwt.Workbook()
            self.sheet = self.wb.add_sheet(sheetName)
            self.count = 0

        def write(self, arr=[]):
            '''

            :param arr:写入的数据->list
            :return: self
            '''
            for i in range(len(arr)):
                self.sheet.write(self.count, i, arr[i])
            self.count = self.count + 1
            return self

        def save(self):
            print("File has been saved:{0}".format(self.path))
            self.wb.save(self.path)

    # 追加数据
    class AddtionWrite():
        def __init__(self, path: str):
            '''

            :param path:文件路径
            '''
            self.path = path
            wb = xlrd.open_workbook(path)
            self.count = wb.sheet_by_index(0).nrows
            self.ws = copy(wb)
            self.sheet = self.ws.get_sheet(0)

        def write(self, arr=[]):
            '''

            :param arr:写入的数据->list
            :return: self
            '''
            for i in range(len(arr)):
                self.sheet.write(self.count, i, arr[i])
            self.count = self.count + 1
            return self

        def save(self):
            print("File has been save:{0}".format(self.path))
            self.ws.save(self.path)

    # read only
    class Cursor():
        __path = None
        __cursorSheet = None
        __index = None

        def __init__(self, path: str):
            '''

            :param path:xls path
            '''
            if path == None:
                print("路径不能为空")
                return
            try:
                s = xlrd.open_workbook(path)
                self.__cursorSheet = s.sheet_by_index(0)
                self.__index = 0
            except Exception as e:
                _logger.error(e)
                # print("errorMsg from jerryExcel:", e)

        def getDataCount(self):
            return self.__cursorSheet.nrows

        def read(self, ignoreFirstLine: bool = True, index: int = 0):
            '''

            :param index:read from the line you define,default 0
            :param ignoreFirstLine: default True
            :return:datas->list
            '''

            if ignoreFirstLine:
                index = 1

            if self.__cursorSheet != None:
                rows = self.__cursorSheet.nrows
                col = self.__cursorSheet.ncols
                datas = []
                count = index

                for i in range(count, rows):
                    data = []
                    for j in range(col):
                        data.append(str(self.__cursorSheet.cell(i, j).value).replace("\n", ""))
                    datas.append(data)

                return datas
