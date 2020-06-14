import re
import json

def read_json_value(json_data,json_path):
    '''
    读取json数据。
    :param json_data: 是json或者能转成json的string类型。
    :param json_path: 自定义的规则。以点分隔。以斜线分隔/
    :return: value,如果path无效，抛错。
    '''
    #校验json_data是json类型数据或者能转成json
    if not isinstance(json_data,dict) and not isinstance(json_data,list) and not isinstance(json_data,str):
        raise AssertionError(str(json_data)+'的类型不是json类型')
    if isinstance(json_data,str):
        try:
            json_data=json.loads(json_data)
        except Exception:
            raise AssertionError(json_data+'的类型不是json类型')
    if not isinstance(json_path,str):
        raise AssertionError('json path必须是string类型')
    json_path_arr=json_path.split('/')
    data=json_data
    path=''
    for item in json_path_arr:
        if item=='':
            continue
        path+=  '/' + item
        if isinstance(data,dict):
            if item not in data:
                raise AssertionError("json path: "+path+" 不存在")
            data=data[item]
        elif isinstance(data,list):
            match=re.search(r'^\d+$',item)
            if match is None:
                raise AssertionError("json path: "+path+" 不存在")
            data=data[int(item)]
        else:
            raise AssertionError("json path: "+path+" 不存在")
    return data
