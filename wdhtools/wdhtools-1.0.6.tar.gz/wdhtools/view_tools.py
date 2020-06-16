#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-09
# @Time: 18:05
# @Name: view_tools

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from featexp import get_univariate_plots, get_trend_stats


def histogram_plot(data, feature):
    """
    利用直方图查看特征数据的具体分布情况(常用来查看目标变量是否符合正态分布)
    :param data: DataFrame | 数据集
    :param feature: string | 特征
    :return:
    """
    sns.distplot(data[feature], kde=False, color='r')


def feature_analysis(data, label, features, bins=10):
    """
    特征与目标相关性分析
    :param data: DataFrame | 数据集
    :param label: string | 标签f
    :param features: list | 特征列表
    :param bins: int | 分组数目, 默认10
    :return: null
    """
    get_univariate_plots(data=data, target_col=label,
                         features_list=features, bins=bins)


def noise_feature_find(train, test, label, features, bins=10, corr=None):
    """
    噪声特征的分析与判断
    :param train: DataFrame | 训练集
    :param test: DataFrame | 测试集
    :param label: string | 标签
    :param features: list | 特征列表
    :param bins: int | 分组数目
    :param corr: float | 选择趋势相关度低于 corr 的特征为噪音特征,默认为 None
    :return: noise_feature_list 噪音特征列表
    """
    get_univariate_plots(data=train, target_col=label, data_test=test,
                         features_list=features, bins=bins)
    if corr is None:
        return None
    else:
        stats = get_trend_stats(data=train, target_col=label, data_test=test)
        noise_feature_list = list(stats[stats.Trend_correlation < corr].Feature)
        return noise_feature_list


def scatter_plot(data, label, feature):
    """
    利用散点图分析变量间的关系(常用来发现某些离散点)
    :param data: DataFrame | 数据集
    :param label: string | 标签
    :param feature: string | 特征
    :return:
    """
    data.plot.scatter(x=feature, y=label, ylim=(0, 1),color='m')
    plt.show()


def matrix_plot(data, features):
    """
    利用 seaborn 对多个特征的散点图、直方图进行整合，得到各个特征两两组合形成的图矩阵(用来查看特征之间的相关性)
    :param data: DataFrame | 数据集
    :param features: list | 特征列表
    :return:
    """
    var_set = features
    sns.set(font_scale=1.25)  # 设置坐标轴的字体大小
    sns.pairplot(data[var_set])  # 可在kind和diag_kind参数下设置不同的显示类型，此处分别为散点图和直方图，还可以设置每个图内的不同类型的显示
    plt.show()


def heat_plot(data):
    """
    利用热力图对各个特征间的关系进行分析
    :param data: DataFrame | 数据集
    :return:
    """
    corr = data.corr()
    f, axis = plt.subplots(figsize=(14, 12))
    sns.heatmap(corr, vmax=0.8, square=True, ax=axis)
    plt.show()


def top_k(data, label, top=10):
    """
    选取与目标变量相关系数最高的K个特征，找出那些相互关联性较强的特征
    :param data: DataFrame | 数据集
    :param label: string | 标签
    :param top: int | 选择最高的K个特征,默认值为10
    :return:
    """
    corr = data.corr()
    k = top
    top10_attr = corr.nlargest(k, label).index
    top10_mat = corr.loc[top10_attr, top10_attr]
    plt.subplots(figsize=(14, 10))
    sns.set(font_scale=1.25)
    sns.heatmap(top10_mat, annot=True, annot_kws={"size": 12}, square=True)
    plt.show()


def spearman(data, label, features):
    """
    采用“斯皮尔曼等级相关”来计算变量与标签的相关性
    :param data: DataFrame | 数据集
    :param label: string | 标签
    :param features: list | 特征列表
    :return:
    """
    spr = pd.DataFrame()
    spr['feature'] = features
    spr['corr'] = [data[f].corr(data[label], 'spearman') for f in features]
    spr = spr.sort_values('corr')
    plt.figure(figsize=(6, 0.25 * len(features)))
    sns.barplot(data=spr, y='feature', x='corr', orient='h')
