# credit to https://blog.csdn.net/farewellnec/article/details/103686077
import re

def trans(rmbAmount):
    '''
    将中文大写金额字符转换成阿拉伯数字。

    参数: rmbAmount 中文大写金额字符

    返回: 转换后的阿拉伯数字
    '''
    chinese_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9}
    chinese_amount = {'分': 0.01, '角': 0.1, '元': 1, '拾': 10, '佰': 100, '仟': 1000, '圆': 1}
    amount_float = 0
    if '亿' in rmbAmount:
        yi = re.match(r'(.+)亿.*', rmbAmount).group(1)
        amount_yi = 0
        for i in chinese_amount:
            if i in yi:
                amount_yi += chinese_num[yi[yi.index(i) - 1]] * chinese_amount[i]
        if yi[-1] in chinese_num.keys():
            amount_yi += chinese_num[yi[-1]]
        amount_float += amount_yi * 100000000
        rmbAmount = re.sub(r'.+亿', '', rmbAmount, count=1)
    if '万' in rmbAmount:
        wan = re.match(r'(.+)万.*', rmbAmount).group(1)
        amount_wan = 0
        for i in chinese_amount:
            if i in wan:
                amount_wan += chinese_num[wan[wan.index(i) - 1]] * chinese_amount[i]
        if wan[-1] in chinese_num.keys():
            amount_wan += chinese_num[wan[-1]]
        amount_float += amount_wan * 10000
        rmbAmount = re.sub(r'.+万', '', rmbAmount, count=1)

    amount_yuan = 0
    for i in chinese_amount:
        if i in rmbAmount:
            if rmbAmount[rmbAmount.index(i) - 1] in chinese_num.keys():
                amount_yuan += chinese_num[rmbAmount[rmbAmount.index(i) - 1]] * chinese_amount[i]
    amount_float += amount_yuan

    return amount_float