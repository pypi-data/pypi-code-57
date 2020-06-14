#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/14 15:23
# @Author   : Dremeue

import csv


class CsvUtils(object):
    """
    CSV工具类
    """

    def __init__(self, csv_file):
        """
        初始化方法, 获取csv文件

        :param csv_file: csv文件路径, 字符串形式传递
        """
        self.csv_file = csv_file

    def write_data(self, header_list, data_list):
        """
        向csv文件中写入数据

        :param header_list: 标题栏数据, 传入可迭代对象(元组/列表都可以), 如('launch_time', 'start_time')
        :param data_list: 与标题栏对应的数据, 也是可迭代对象, 且对象中的子元素也需要是可迭代对象,如(('1', '6'), ('2', '7'))
        :return:
        """

        # 创建csv对象
        csv_obj = open(self.csv_file, 'w', newline='')
        writer = csv.writer(csv_obj)

        # 整合标题栏数据和对应的数据
        res_list = [header_list]
        res_list.extend(data_list)

        # 向csv文件中写入数据
        writer.writerows(res_list)

        # 关闭csv对象
        csv_obj.close()


if __name__ == '__main__':
    pass

    # 测试数据, 可打开验证
    """
    csvUtils = CsvUtils('tinyutils.csv')
    csvUtils.write_data(header_list=['launch_time', 'start_time'], data_list=(['123', '666'], ['234', '777']))
    """
