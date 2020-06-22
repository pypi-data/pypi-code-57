# coding:utf-8
"""*--撒哈la--*"""

import re

"""
数据校验器 Validator_Sahala
可校验最外层字典 嵌套各种列表字典的key和value的具体值或可变value的type类型
校验任意 int str float bool list set tuple 数据类型
list正则校验值或值type中str,int float,不能校验具体值
expect 预期正则匹配关键字: re$+正则表达式，每次正则匹配正确与否停止当前值继续下一步校验
"""


class Validator_Sahala():

    def assert_re_Expression_data(self, key, expect_Expression, resp_value, error_msg):
        """
        如果except中包含re$就与response做正则匹配，否则正常比对，不做type校验
        :param expect_Expression: 正则表达式
        :param resp_value: value正则匹配必须是字符串
        """
        if expect_Expression not in (int, str, float):  # 先过滤type校验，跳出本方法后下一步校验type类型
            if 're$' in str(expect_Expression) and type(expect_Expression) is str:  # 只保留包含re$的字符串
                re_data = str(expect_Expression).replace('re$', '')  # 替换字符串中关键字re$提取正则表达式
                if re.match(re_data, str(resp_value)):  # 正则表达式匹配字符串
                    print('27 pass 正则匹配校验成功 expect_Expression中 %s == response中 %s' % (re_data, resp_value))
                    return True  # 正则校验成功后就不去继续校验相等，否正会比对失败，抛出不必要的异常
                else:
                    print('30 fail 正则匹配校验失败 expect_Expression中 %s != response中 %s' % (re_data, resp_value))
                    print(error_msg)
                    raise Exception(error_msg)  # 失败后抛异常
            elif expect_Expression == resp_value:
                print('34 pass: %s 值校验：expect中 %s == response中 %s' % (key, expect_Expression, resp_value))
                return True  # 相等时必须True否则，后面else语句直接抛异常，函数内部可以return不影响后面数据比对，反之主函数不能return

    def is_dict_or_None_dict(self, expect, response, error_msg):
        """
        在所有循环字典前，或循环出的value是字典时，先校验空字典或非空
        :param expect:
        :param response:
        """
        if isinstance(expect, dict) and isinstance(response, dict):  # 非字典进入主程序下一步
            if dict(expect) == {} and dict(response) == {}:  # 校验返回空
                print("45 pass expect: %s == response: %s" % (expect, response))
            elif dict(expect) != {} and dict(response) == {} or dict(expect) == {} and dict(
                    response) != {}:  # 预期不为空但返回空 or #预期空但返回不为空
                print("48 fail expect: %s != response: %s" % (expect, response))
                print(error_msg)
                raise Exception(error_msg)

    def is_dict_or_other(self, expe_res):
        """
        对传入的expect和response数据分类转换
        :param expe_res:
        :return:
        """
        try:
            if isinstance(expe_res, dict):  # 如果是字典用dict转
                dict_data = dict(expe_res)
            else:
                dict_data = eval(expe_res)  # 如果是读取的json字符串用eval转字典
            return dict_data
        except:
            return expe_res  # 非dict和json字符串直接返回比对

    def __list_value_assert(self, e_k, r_k, e_v, r_v, error_msg):
        """
        list中只做type数据类型校验 int str float dict set等
        :param e_k:
        :param r_k:
        :param e_v:
        :param r_v:
        """
        if self.assert_re_Expression_data(e_k, e_v, r_v, error_msg):  # 如果内部未抛异常或None未筛选，继续下一个if. 正则校验或值比对e_v == r_v
            pass
        if e_v == type(r_v):  # list中的type校验
            print('78 pass: value list type 校验: expect中 %s: %s == response中 %s: %s' % (e_k, e_v, r_k, r_v))
        elif e_v == r_v:  # list中值判断
            print('80 pass: value list 值校验: expect中 %s: %s == response中 %s: %s' % (e_k, e_v, r_k, r_v))
        # 排除类型和值,排除[]校验与后面重复，忽略列表已结束的正则
        if e_v not in (int, str, float) and not isinstance(e_v, int):
            if 're$' not in str(e_v) and type(e_v) != type(r_v) != list:
                print('84 fail: value list expect中 %s: %s != response中 %s: %s' % (e_k, e_v, r_k, r_v))
                print(error_msg)
                raise Exception(error_msg)
        elif e_v != type(r_v) and e_v != r_v:
            print('88 fail: value list type 校验: expect中 %s: %s != response中 %s: %s' % (e_k, e_v, r_k, r_v))
            print(error_msg)
            raise Exception(error_msg)

    def __dict_assert(self, e_dict, r_dict, error_msg):
        """
        dict校验主方法比对两个value中的dict的key,value
        :param e_dict:
        :param r_dict:
        """
        self.is_dict_or_None_dict(e_dict, r_dict, error_msg)  # 循环前先校验空字典，expect,response都非空{}继续执行
        e_dic = self.is_dict_or_other(e_dict)  # 对循环出的字典转换
        r_dic = self.is_dict_or_other(r_dict)
        for e_key, e_valuetype in e_dic.items():
            for r_k, r_v in r_dic.items():
                r_type = type(r_v)
                if e_key in r_dic.keys():
                    self.__dict_or_list_assert(e_key, r_k, e_valuetype, r_v, error_msg)  # 校验返回value中的dict和list中dict
                    if e_key == r_k:
                        print('107 pass: key值校验：expect中 %s == response中 %s' % (e_key, r_k))
                        if self.assert_re_Expression_data(e_key, e_valuetype, r_v,
                                                          error_msg):  # 正则校验或值比对e_valuetype == r_v
                            pass
                        elif e_valuetype == r_type:
                            print('112 pass: value type校验: expect中 %s: %s == response中 %s: %s' % (
                                e_key, e_valuetype, r_k, r_type))
                        elif self.__list_value_assert(e_key, r_k, e_valuetype, r_v, error_msg):
                            pass  # 最后校验list type前，列表比对
                        elif r_type == list and type(e_valuetype) == list:  # 最后校验嵌套list
                            print('117 pass: list type 校验: expect中 %s: %s == response中 %s: %s' % (
                                e_key, e_valuetype, r_k, r_type))
                        elif self.is_dict_or_None_dict(e_valuetype, r_v, error_msg):  # 校验循环出的value为空{}dict
                            pass  # 最后校验嵌套dict前，排除校验不到的空dict
                        elif r_type == dict and type(e_valuetype) == dict:  # 最后校验嵌套dict
                            print('122 pass: value dict type 校验: expect中 %s: %s == response中 %s: %s' % (
                                e_key, e_valuetype, r_k, r_type))
                        else:
                            print(
                                '126 fail: expect中 { %s: %s } != response中 { %s: %s }' % (e_key, e_valuetype, r_k, r_v))
                            print(error_msg)
                            raise Exception(error_msg)
                else:
                    print(
                        '131 fail: expect中的：{ %s: %s } ； 在response中未找到: { %s: %s }' % (e_key, e_valuetype, r_k, r_v))
                    print(error_msg)
                    raise Exception(error_msg)

    def __dict_or_list_assert(self, e_key, r_key, e_list, r_list, error_msg):
        """
        比对两个list中的dict或dict中的key,value
        :param e_key:
        :param r_key:
        :param e_list:
        :param r_list:
        """
        if e_key == r_key:  # 筛选多个字典和多个列表的key相同时再对应比对value
            if type(e_list) == list and type(r_list) == list:
                e_l = list(e_list)
                for i in range(len(e_l)):
                    global e_dict
                    e_dict = e_l[i]
                r_l = list(r_list)
                for ii in range(len(r_l)):
                    r_dict = r_l[ii]
                    if type(e_dict) != dict and type(r_dict) != dict:
                        self.__list_value_assert(e_l, r_l, e_dict, r_dict, error_msg)
                    else:
                        self.__dict_assert(e_dict, r_dict, error_msg)
            elif type(e_list) == dict and type(r_list) == dict:
                e_dict = e_list
                r_dict = r_list
                self.__dict_assert(e_dict, r_dict, error_msg)

    # 校验器主方法
    def __Validator(self, expect_, response_, error_msg):
        """
        校验两个字典key和value或者value的type类型
        :param expect_:
        :param response_:
        """
        expect = self.is_dict_or_other(expect_)
        response = self.is_dict_or_other(response_)
        types = (str, int, float, bool, list, set, tuple)  # 可直接比对对象，特例 None
        if type(expect) in types or type(response) in types or None in (expect, response):  # 只要有一个不是字典就直接比对
            if expect == response:
                print('173 pass: expect中 %s == response中 %s' % (expect, response))
            else:
                print('175 fail: expect中 %s != response中 %s' % (expect, response))
                print(error_msg)
                raise Exception(error_msg)
        else:
            self.__dict_assert(expect, response, error_msg)  # 字典校验方法，及主要校验逻辑

    def data_validator(self, expect, response, error_msg):
        """
        数据校验器主调用方法
        :param expect:
        :param response:
        """
        print("\n\n================Data Validator START !================\n\n")
        self.__Validator(expect, response, error_msg)
        print("\n\n================Data Validator FINISH !================\n\n")


# if __name__ == '__main__':
    # 字典 多层嵌套
    # response_ = {"count":33,"nas":{"name":{"name1":"jod","age":{"ag":18}}}}
    # expect_ = {"count":int,"nas":{"name":{"name1":str,"age":{"ag":int}}}}

    # list 嵌套相同key的字典，以及list中验证str和int不能验证str和int的具体值,
    # response_ = {"names":["1","2","3"],"jod":[1,2,3],"age":{"agee":[{"key":1},{"key":1}]},"pople":[{"1":1}]}
    # expect_ = {"names":[str],"jod":[int],"age":{"agee":[{"key":int}]},"pople":[{"1":1}]}

    # 校验key对应的value实际值相等
    # response_ = {"name": {"n": 123}, "age": [11, 22, 1222]}
    # expect_ = {"name": {"n": 're$^\d[1-2]'}, "age": ['re$^\d[1-2]']}

    # 校验任意 int str float bool list set tuple,None
    # response_ = None
    # expect_ = None
    # response_ = False
    # expect_ = True
    # expect_ = {"v": {"b": int}}
    # response_ = {"v": {"a": 33}}
    # response_ = {"ss":33}  #bool校验使用字典嵌套
    # expect_ = {"ss":int}

    # list正则校验值或值类型校验
    # response_ = {"n": [123, 22, 111111, 12121212, 222, "12"]}
    # expect_ = {"n": ['re$\d']}
    # expect_ = {"n": [int]}

    # s = Validator_Sahala()
    # s.data_validator(expect_, response_, "断言失败")

# 校验结果：
# [2019-08-17 16:39:54,916] - log_common.py] - INFO:
# ================Data Validator START !================
# [2019-08-17 16:39:54,918] - log_common.py] - INFO: 163 pass: expect_中 False == response_中 False
# [2019-08-17 16:39:54,918] - log_common.py] - INFO:
# ================Data Validator FINISH !================
