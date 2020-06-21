import re
from rfApiTestLibrary import jsonpath
def json_path_regular_match(json_data,json_path,pattern_str):
    '''
    json通过json path获取值是否符合正则匹配。
    :param json_data: json类型。
    :param json_path: json路径，string类型
    :param pattern_str: string类型
    :return:
    '''
    if not isinstance(json_data,dict) and not isinstance(json_data,list):
        raise AssertionError(json_data+"不是list或者dict类型")
    value = jsonpath.read_json_value(json_data, json_path)
    value = str(value)
    match=re.search(pattern_str,value)
    if match is None:
        raise AssertionError(pattern_str+" ,匹配失败: "+str(value))

def str_regular_match(data_str,pattern_str):
    '''
    是否正则匹配。
    :param data_str:
    :param pattern_str:
    :return:
    '''
    match = re.search(pattern_str, data_str)
    if match is None:
        raise AssertionError(pattern_str+" ,匹配失败: "+str(data_str))
