'''
Documentation: 处理基本数据:字典，列表的.
对基础类的封装。对字典和列表和元组等的处理。
引用包名是atBasicLibrary，引用本python文件，请使用Library  atBasicLibrary/basic.py.
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   atBasicLibray/keywords/[ ../keywords/sc/basic.html | basic.robot ],
文档在[ ../keywords/basic.doc.html | 这里 ]。
'''

def at_should_be_none(obj,message=None):
    '''
    校验obj是None,如果不是None,报错
   【obj】: 任何类型
   【message】: 设定出错了，返回的错误信息

    目前使用该方法的关键字是:
    [../keywords/basic.doc.html#Should%20Be%20None | Should be none],
    [../keywords/basic.doc.html#验证是None | 验证是None],

    Examples:
        | 关键字             |  参数    |      参数     |
        | at should be none |  ${None} | 出错的message |
        | at should be none |  ${123} |  出错的message |
    '''
    if obj is not None:
        if message is None:
            raise AssertionError(str(obj)+' is not None!')
        else:
            raise AssertionError(message)

def at_should_not_be_none(obj,message=None):
    '''
    校验obj不是None,如果是None,报错
   【obj】: 任何类型
   【message】: 设定出错了，返回的错误信息

   目前使用该方法的关键字是:
    [../keywords/basic.doc.html#Should%20Not%20Be%20None | Should not be none],
    [../keywords/basic.doc.html#验证不是None | 验证不是None],

   Examples:
        | 关键字                  |  参数    |      参数     |
        | at should not be none  |  ${None} | 出错的message |
        | at should not be none  |  ${123}  | 出错的message |
    '''
    if obj is None:
        if message is None:
            raise AssertionError('It is None!')
        else:
            raise AssertionError(message)