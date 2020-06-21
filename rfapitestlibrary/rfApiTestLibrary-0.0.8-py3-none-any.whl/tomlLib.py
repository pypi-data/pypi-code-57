'''
Documentation: 对toml文件内容中值的处理。
引用包名是atBasicLibrary，引用本python文件，请使用Library  atBasicLibrary/tomlLib.py。
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   atBasicLibray/keywords/[ ../keywords/sc/toml.html | toml.robot ],
'''

import toml
import os

def at_get_toml_file(toml_file_path):
    '''
    通过指定toml文件，把文件内容以字典格式返回。
    :param toml_file_path:  String类型,toml文件路径,绝对路径或者相对路径都可以
    :return:  指定toml文件中的内容, 返回值是字典类型

     目前使用该方法的关键字是:
    [../keywords/toml.doc.html#获取toml文件 | 获取toml文件],
    [../keywords/toml.doc.html#Get%20toml | Get toml],

     Examples:
         |     关键字        |           参数        |
         | at get toml file |  <文件相对或者绝对路径>  |
    '''
    if not os.path.exists(toml_file_path):
        raise AssertionError("[ %s ]文件路径不存在" % toml_file_path)
    toml_config = toml.load(toml_file_path)
    return toml_config

def at_get_toml_value(toml_content, key):
    '''
    :param toml_content:  从指定的toml文件中获取的内容，为字典类型
    :param key:  String类型,key值
    :return:  返回toml中指定的值，类型可以是toml中的任何类型。

     目前使用该方法的关键字是:
    [../keywords/toml.doc.html#从toml里取值 | 从toml里取值 ],
    [../keywords/toml.doc.html#Get%20value%20from%20toml | Get value from toml ],

    Examples:
         |        关键字      |  参数            | 参数    |
         | at get toml value |  <toml config>   | <key>  |
    '''
    if toml_content is None:
        raise AssertionError("toml内容是None")
    key_list=key.split(".")
    for item in key_list:
        try:
            toml_content = toml_content[int(item)]
        except ValueError:
            toml_content=toml_content[item]
    return toml_content

def at_get_value_from_toml_file(toml_file_path, key):
    '''
    :param toml_file_path:  String类型,toml文件路径,绝对路径或者相对路径都可以
    :param key:  String类型,key值
    :return:  返回toml中指定的值，类型可以是toml中的任何类型。

    目前使用该方法的关键字是:
    [../keywords/toml.doc.html#从toml文件里取值 | 从toml文件里取值 ],
    [../keywords/toml.doc.html#Get%20the%20value%20from%20toml%20file | Get the value from toml file ],

    Examples:
         |   关键字                        |  参数                         | 参数    |
         | at get value from toml file    | <toml文件相对路径或者绝对路径>   |  <key>  |
    '''
    toml_config=at_get_toml_file(toml_file_path)
    return at_get_toml_value(toml_config,key)

