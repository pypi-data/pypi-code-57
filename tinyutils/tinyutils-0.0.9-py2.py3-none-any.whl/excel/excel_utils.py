#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/11 17:26
# @Author   : Dremeue


from openpyxl import *
import re


class ExcelUtils:
    """
    Excel的工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def get_area_data(excel_name, start_cell, end_cell, sheet_name=None):
        """以列表的形式, 返回excel文件的指定区域的内容

        :param excel_name: excel文件位置
        :param start_cell: 起始单元格(左上角单元格)
        :param end_cell: 终止单元格(右下角单元格)
        :param sheet_name: 工作表名称(不传入时, 默认取第一张工作表)
        :return: 列表对象

        """
        wb = load_workbook(excel_name)

        if sheet_name is None:
            sheet_obj = wb.active
        else:
            sheet_obj = wb.get_sheet_by_name(sheet_name)

        # 获取循环的行
        row_index_start = int(re.sub("\D", "", start_cell))
        row_index_end = int(re.sub("\D", "", end_cell))

        # 获取循环的列
        column_index_start = len(sheet_obj["A1": start_cell][0])
        column_index_end = len(sheet_obj["A1": end_cell][0])

        # 定义需返回的列表对象
        cells_list = []

        for i in range(row_index_start, row_index_end + 1):
            cell_list_temp = []
            for j in range(column_index_start, column_index_end + 1):
                cell_list_temp.append(sheet_obj.cell(row=i, column=j).value)
                cells_list.append(cell_list_temp)

        return cells_list
