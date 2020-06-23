import json


def load_json(json_file_path):
    """
    读取json文件转dict or list(dict)
    :param json_file_path:
    :return:
    """
    with open(json_file_path, encoding='utf-8', mode='r') as f:
        return json.load(f, encoding='utf-8')


def obj2jsonstr(obj: object, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False):
    """
    对象转json str
    :param obj:
    :return:
    """
    return json.dumps(obj, default=default, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)
