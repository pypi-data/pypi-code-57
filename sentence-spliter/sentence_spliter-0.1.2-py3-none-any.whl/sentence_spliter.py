# -*- coding:utf-8 -*-
# CREATED BY: Li Wang
# CREATED ON:2020/4/30 上午11:56
# LAST MODIFIED ON:
# AIM: 对划分好的句子长短句做处理
from sentence_spliter import spliter
import re
from typing import List
from sentence_spliter.time_it import time_measure


class Spliter:
    def __init__(self, options):
        if options['language'] == 'zh':
            self.spliter = spliter.Spliter('zh')
            self.flag = 'zh'
        elif options['language'] == 'en':
            self.spliter = spliter.Spliter('en')
            self.flag = 'en'
        self.remove_blank_on = options['remove_blank']
        # -- parameter -- #
        self.long_short_sent_handle = options['long_short_sent_handle']
        self.max_length = options['max_length']
        self.min_length = options['min_length']
        self.hard_max_length = options['hard_max_length']
        self.long_filter = re.compile('([.?!。？！，,])')

    @time_measure
    def cut_to_sentences(self, text):
        text = re.sub(r'\s+','',text) #先不考虑中英文混合情况
        if self.remove_blank_on:
            all_sentence = self.to_sentence(text)
        if self.flag == 'en':
            return all_sentence
        elif self.flag == 'zh':
            if self.long_short_sent_handle == 'y':
                return self.refine(all_sentence)
            else:
                return all_sentence

    # - step 1:划分句子
    def to_sentence(self, paragraph) -> [str]:
        sentences = self.spliter.cut_to_sentences(paragraph)
        return sentences

    def refine_single_short(self, sentence: str) -> [str]:
        pass

    # - step 2:对过长过短句子做处理
    @time_measure
    def refine(self, all_sentence: List[str]) -> [str]:
        out = []
        i = 0
        length = len(all_sentence)
        end_sntnc = ''
        while i < length:
            if not end_sntnc:
                sent = all_sentence[i]
            else:
                sent = end_sntnc + all_sentence[i]

            if self.is_valid_sntnc(sent):
                out.append(sent)
            else:
                out.extend(self.refine_single(sent))
                end_sntnc = ''
                if len(out[-1]) < self.min_length: #self.is_valid_sntnc(out[-1]):
                    end_sntnc = out[-1]
                    out = out[0:-1]
            i += 1
        if end_sntnc:
            out.append(end_sntnc)
        return out

    def is_valid_sntnc(self, sentence: str):
        '''
        判断是否满足正常句子，长度在15到150之间
        :param sentence:
        :return:
        '''
        if self.min_length < len(sentence) < self.max_length:
            return True
        else:
            return False

    def refine_single(self, sentence: str) -> List[str]:
        '''
        :param sentence:
        :return:
        '''
        pattern_w = re.compile('([?\!\.…;？！。……；,,])')
        out = ['']
        pre_spilt_id = 0
        for i, word in enumerate(sentence):
            if not (i > 0 and pattern_w.match(sentence[i - 1])):
                out[-1] = out[-1] + word
            else:
                if len(out[-1]) <= self.max_length:
                    out[-1] = out[-1] + word
                    pre_spilt_id = i
            # -- run hard max -- #
            if len(out[-1]) > self.hard_max_length:
                if pre_spilt_id <= 0:
                    pre_spilt_id = self.hard_max_length
                range = len(out[-1]) - i + pre_spilt_id - 1
                if range <= self.min_length:
                    range = self.hard_max_length
                    pre_spilt_id = i
                shorter = out[-1][0: range]
                sub = sentence[pre_spilt_id:i + 1]
                out[-1] = shorter
                out.append(sub)
        return out

    def remove_blank(self, sentence: str) -> str:
        if not self.remove_blank_on:
            return sentence
        else:
            pass
    # -- 中英文混合情况 -- #
    # def is_zh(self, _char: str) -> bool:
    #     if '\u4e00' <= _char <= '\u9fa5':
    #         return True
    #     return False
    #
    # def len(self, sentence:str) -> bool:
    #     '''
    #     只考虑英语和中文情况
    #     :param sentence:
    #     :return:
    #     '''
    #     cnt = 0
    #     nzh_flag = 0
    #     for char in sentence:
    #         if self.is_zh(char):
    #             cnt += 1
    #             nzh_flag = 0
    #         else:
    #             nzh_flag
    #
    # def is_zh_sntnc(self, sentence: str) -> bool:
    #     length = len(sentence)
    #     count = None
    #     for c in sentence:
    #         pass
