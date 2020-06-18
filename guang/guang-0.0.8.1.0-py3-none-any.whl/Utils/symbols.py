import string
import re

useless = string.printable + "，。；’：‘’“”！？《》￥…（）—·【】、"


def has_chinese(str0):
    """判断是否存在汉字
    """
    return bool(re.search(u'[\u4e00-\u9fa5]', str0))


def has_english(str0):
    return bool(re.search('[a-z]', str0.lower()))


def has_number(str0):
    return bool(re.search('[0-9]', str0))


def replace_bracket(a):
    l0 = a.find('（')
    l1 = a.find('）')
    a = a.replace(a[l0:l1 + 1], '')
    return a


def sub2empty(useless, str0):
    return re.sub(f"[{useless}]+", "", str0)


def fstring(string, N=20, align='>', symbol=None, flag='en'):
    """Chinese and English mixed string alignment
     chr(12288): Chinese space"""
    if flag == 'zh':
        space = chr(12288)  # chinese space
    elif flag == 'en':
        space = chr(32)  # english space

    def lenStr(string, space):  # if space is chr(12288)
        if space == chr(12288):
            zh, en = 1, 0.6
        elif space == ' ':
            zh, en = 1.83, 1
        count = 0
        for i in string:
            if has_chinese(i):
                count += zh
            else:
                count += en
        return count

    n = round(lenStr(string, space))
    if symbol == None:
        symbol = space
    if align == '>':
        out = (N - n) * symbol + string
    elif align == "<":
        out = string + symbol * (N - n)
    elif align == "^":
        left = (N - n) // 2
        right = N - n - left
        out = left * symbol + string + right * symbol
    else:
        "align options: > < ^"
    return out


if __name__ == "__main__":
    # print(useless)
    a = """阿斯顿发生啊空手ssssssdfasd道解为了阿萨；爱哭的时间斯京东方"""
    b = """绿卡就是asdfasdf咔叽"""
    print(fstring(a, 100, '>', flag='en'))
    print(fstring(b, 100, '>', flag='en'))
    print(fstring(a, 50, '>', flag='zh'))
    print(fstring(b, 50, '>', flag='zh'))
