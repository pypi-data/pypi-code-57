'''
Documentation: 利用robot framework的一些机制获其信息。
对robot framework特殊处理的封装
引用包名是atApiBasicLibrary，引用本python文件，请使用Library  atApiBasicLibrary/rft.py。
'''
import rfApiTestLibrary.log as atLogger
import re

def at_is_rft_variable_exists(rft_variable, variable):
    '''
    基础方法，校验是robotframework 命令行中--variable  <variable>:<value>。<variable>是不是存在。
    【rft_variable】: 不是String类型，是Robot framework特有的一种类型
    【variable】: String类型，不需要添加'$'生命变量，因为代码会自动补齐
    RETURN: boolean类型
    底层方法，不建议使用。

    Examples:
         |  命令行                            |   关键字                   |    参数               |     参数    |  结果    |
         | --variable  aa=1  --variable bb:2 | at is rft variable exists | 通过Get Variables获得  |   aa       | ${True}  |
         | --variable  aa=1  --variable bb:2 | at is rft variable exists | 通过Get Variables获得  |   ww       | ${False} |
    '''
    if rft_variable is None:
        return False
    searchScope = re.search('\$\{'+variable+'\}', str(rft_variable),re.IGNORECASE)
    if (searchScope) is None:
        return False
    return True

def at_get_rf_variable_value(project_dictionary_variable,variable,local_variable):
    '''
     当命令行--variable  <variable>:<value>。<variable>是存在的，就返回<variable>，否则返回local_variable
    【project_dictionary_variable】: 不是String类型，是Robot framework特有的一种类型
    【variable】:  String类型，不需要添加'$'生命变量，因为代码会自动补齐
    【local_variable】:本地的变量值，理论上是任意类型
     RETURN: variable 或者  local_variable

     Examples:
         |  命令行                            |   关键字                  |    参数               |     参数    |    参数    |   结果  |
         | --variable  aa=1  --variable bb:2 | at get rf variable value | 通过Get Variables获得  |   aa       |    123     |   1    |
         | --variable  aa=1  --variable bb:2 | at get rf variable value | 通过Get Variables获得  |   ww       |    123     |   123  |
    '''
    if  project_dictionary_variable is None  or variable is None  or at_is_rft_variable_exists(project_dictionary_variable,variable) is False:
        atLogger.debug("没有在运行命令加入--variable或者是传参不存在")
        return local_variable
    return project_dictionary_variable['${'+variable+'}']