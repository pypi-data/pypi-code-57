'''
Documentation: 处理json包含关系的方法
'''
import json_tools
import rfApiTestLibrary.log as log
import re
def json_contain_sub_json(son_json, father_json):
    '''
    父亲json包含儿子json。父亲一般来说就是实际结果，儿子一般是期待的结果
    :param father_json: json类型
    :param son_json: json类型
    '''
    result = json_tools.diff(son_json, father_json)
    if not isinstance(result,list):
        raise AssertionError("json_tools的返回结果不是list,有可能是输入数据有误！")
    msg="两个json对比结果: "+str(result)
    log.info(msg, html=True, also_console=True)
    if result==[]:
        log.info("两个json完全相同",html=True, also_console=True)
        return
    for item in result:
        if not isinstance(item,dict):
            raise AssertionError("json_tools的返回结果具体内容不是字典,有可能是输入数据有误！")
        #不处理'add'，只处理'remove'，'replace'
        if 'remove' in item:
            raise AssertionError(msg)
        if 'replace' in item:
            raise AssertionError(msg)

def json_contains_not_orderd_sub_json(son,father):
    '''
    父亲json包含儿子json。父亲一般来说就是实际结果，儿子一般是期待的结果。此方法
    支持list无序包含。但是不支持list内部包含嵌套。
    :param son:
    :param father:
    :return:
    '''
    result = json_tools.diff(son, father)
    lst = []
    if not isinstance(result,list):
        raise AssertionError("json_tools的返回结果不是list,有可能是输入数据有误！")
    msg="两个json对比结果: "+str(result)
    if result==[]:
        return
    for item in result:
        if not isinstance(item,dict):
            raise AssertionError("json_tools的返回结果具体内容不是字典,有可能是输入数据有误！")
        #不处理'add'，只处理'remove'，'replace'
        if 'remove' in item:
            raise AssertionError(msg)
        if 'replace' in item:
            pattern_str = '/\d+'
            pattern = re.compile(pattern_str)
            value_list = pattern.findall(item['replace'])
            if value_list==[]:
                raise AssertionError(msg)

            temp_start = 0
            temp_str = ''
            for value_item in value_list:
                index = item['replace'].index(value_item, temp_start)
                temp_str = temp_str + item['replace'][temp_start:index]
                if not temp_str in lst:
                    for lst_item in lst:
                        if lst_item.index(temp_str)==0 or temp_str.index(lst_item)==0:
                            raise AssertionError("不支持超过1层的list比较")
                    lst.append(temp_str)
                temp_start = index + len(value_item)
    for lst_item in lst:
        son_data=parse_json_by_path(son,lst_item)
        father_data=parse_json_by_path(father,lst_item)
        son_data_length=len(son_data)
        father_data_length = len(father_data)
        if son_data_length>father_data_length:
            raise AssertionError(msg)
        for son_data_item in son_data:
            match1=set()
            for father_data_item in father_data:
                match2=set()
                for son_key,son_value in son_data_item.items():
                    if son_key not in father_data_item:
                        match2.add(False)
                        break
                    father_value = father_data_item[son_key]
                    if type(father_value) != type(son_value):
                        match2.add(False)
                        break
                    if isinstance(son_value,list):
                        match2.add(False)
                        raise AssertionError("不支持超过1层的list比较")
                    if isinstance(son_value, str) or isinstance(son_value, bool) or isinstance(son_value,int) or isinstance(son_value, float):
                        if son_value != father_value:
                            match2.add(False)
                            break
                        match2.add(True)
                if len(match2)==0 or False in match2:
                    continue
                if True in match2:
                    match1.add(True)
                    break
            if len(match1)==0:
                raise AssertionError(msg)
                break



def parse_json_by_path(json,path):
    '''

    :param json:
    :param path:
    :return:
    '''
    arr=path.split('/')
    new_json=json
    for item in arr:
        if item=='':
            continue
        pattern_str = '\d+'
        pattern = re.compile(pattern_str)
        value_list = pattern.findall(item)
        if len(value_list)!=0:
            new_json=new_json[int(value_list[0])]
            continue
        new_json=new_json[item]
    return new_json
