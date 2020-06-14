#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/11 16:46
# @Author   : Dremeue

from pyecharts.charts import Line
from pyecharts import options as opts


class EchartsUtils(object):
    """
        Echarts工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def get_basic_line(xaxis_data, series_name, yaxis_data, line_title=None, line_subtitle=None,
                       html_name="line.html"):
        """
        生成简单折线图的html文件

        PS:
            1. 暂不生成折线图的图片文件, 测试官方推荐的`make_snapshot`, 效率较低且需要手动关闭chromedriver.exe, 故不加入此功能
            2. 由于生成的html文件引用的js文件访问较慢, 需耐心等待几秒或使用梯子, 可快速访问

        :param xaxis_data: 列表形式传递, x轴坐标数据
        :param series_name: 列表形式传递, 折线对象的名称
        :param yaxis_data: 列表形式传递, y轴坐标数据(数量需和折线名称)
        :param line_title: 图表的主标题
        :param line_subtitle: 图表的副标题
        :param html_name: 生成的折线图的html文件, 默认为line.html
        :return:
        """
        # 生成折线图对象
        bar = Line()

        # 绑定x轴数据
        bar.add_xaxis(xaxis_data)

        # 绑定每条折线的名称和数据
        index = 0
        for line_name in series_name:
            bar.add_yaxis(line_name, yaxis_data[index])
            index += 1

        # 设置图表的标题
        bar.set_global_opts(title_opts=opts.TitleOpts(title=line_title, subtitle=line_subtitle))

        # 生成html文件和截图
        bar.render(html_name)


if __name__ == '__main__':
    pass

    """
    测试get_basic_line方法, 可手动打开进行测试
    """
    """
    EchartsUtils.get_basic_line(['a', 'b', 'c', 'd', 'e', 'f'], ['商家a', '商家b'],
                                [[5, 20, 36, 10, 75, 90], [11, 10, 40, 33, 55, 70]], line_title='tinyutils主标题',
                                line_subtitletle='tinyutils副标题', html_name='tinyutils.html')
    """
