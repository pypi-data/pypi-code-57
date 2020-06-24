#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import string
import enum


class StopWordType(enum.Enum):
    """停用词类型"""
    PUNCTUATION = string.punctuation + "℃￥！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."
    NUMBER = '0123456789０１２３４５６７８９'
    TAB = '\t　'
    ALL = PUNCTUATION + NUMBER + TAB


def remove_stop_word(input_string, stop_word_type_list):
    """
    去掉停用词 停用词使用空格作为占位符
    :param input_string: 输入的字符串
    :type input_string: str
    :param stop_word_type_list: 停用词的list
    :return: string
    """
    if type(stop_word_type_list) is not list or len(stop_word_type_list) == 0:
        raise TypeError('stop_word_type_list is not list or is empty')

    for stop_word_type in stop_word_type_list:
        if stop_word_type not in StopWordType:
            raise TypeError('stop_word_type_list is not StopWordType')

    if type(input_string) is not str:
        raise TypeError('input_string is not string')

    # 合并停用词
    if StopWordType.ALL in stop_word_type_list:
        # 如果用户选择了ALL 则不需要拼接停用词
        stop_word = set(StopWordType.ALL.value)
    else:
        stop_word = ''
        for stop_word_type in stop_word_type_list:
            stop_word += stop_word_type.value
        stop_word = set(stop_word)

    # 停用词使用空格作为占位符
    result_list = list()
    for char in input_string:
        if char not in stop_word:
            result_list.append(char)
        else:
            result_list.append(' ')

    return ''.join(result_list)
