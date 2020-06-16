#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-05
# @Time: 11:17
# @Name: sklearn_tools
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA

"""
1. one_hot 独热编码
2. label_encoder  标签编码

"""


def one_hot_transform(data, feature, result):
    """
    将类别特征根据 onehot 编码之后的结果， 插入到原有数据集
    :param data:
    :param feature:
    :param result:
    :return:
    """
    nums = result.shape[1]
    for i in range(nums):
        feature_name = feature + str(i)
        data[feature_name] = result[:, i]
    return data


def one_hot(data, feature):
    """
    独热编码, 返回编码模型，以及编码之后的数据集
    :param data: 操作数据集
    :param feature: 类别特征
    :return:
    """
    model = OneHotEncoder(handle_unknown='ignore')
    model.fit(data[[feature]])
    result = model.transform(data[[feature]]).toarray()
    data = one_hot_transform(data, feature, result)
    return model, data


def label_encoder(data, feature):
    """
    标签编码
    :param data: 操作数据集
    :param feature: 类别特征
    :return:
    """
    model = LabelEncoder()
    model.fit(data[feature])
    data[feature] = model.transform(data[feature])
    return model, data


def std(data, feature):
    """
    数据标准化
    :param data: 操作数据集
    :param feature: 数值特征
    :return:
    """
    model = StandardScaler()
    model.fit(data[feature].values.reshape(-1, 1))
    data[feature] = model.transform(data[feature].values.reshape(-1, 1))
    return model, data


def min_max(data, feature):
    """
    数据归一化
    :param data: 操作数据集
    :param feature: 数值特征
    :return:
    """
    model = MinMaxScaler()
    model.fit(data[feature].values.reshape(-1, 1))
    data[feature] = model.transform(data[feature].values.reshape(-1, 1))
    return model, data


def pca(data, n_components=0.99):
    """
    pca 将维
    :param data: DataFrame | 标准化后的数据集
    :param n_components: float | 信息占比,默认 0.99
    :return: 降维后的数据集
    """
    model = PCA(n_components=n_components)
    model.fit(data)
    print("保留各个特征的方差百分比")
    print(model.explained_variance_ratio_)
    print("保留的特征个数")
    print(model.n_components_)
    new_data = model.transform(data)
    return model, new_data
