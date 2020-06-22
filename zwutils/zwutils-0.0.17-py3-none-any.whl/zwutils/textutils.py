
def is_chinese(c):
    '''https://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode'''
    if u'\u4E00' <= c < u'\u9FFF' or \
       u'\u3400' <= c < u'\u4DBF' or \
       u'\u20000' <= c < u'\u2A6DF' or \
       u'\u2A700' <= c < u'\u2B73F' or \
       u'\u2B740' <= c < u'\u2B81F' or \
       u'\u2B820' <= c < u'\u2CEAF':
        return True
    else:
        return False

def is_chinese_punctuation(c):
    arr = [
        u'\u3002',u'\uFF1F',u'\uFF01',u'\u3010',u'\u3011',u'\uFF0C',u'\u3001',u'\uFF1B',
        u'\uFF1A',u'\u300C',u'\u300D',u'\u300E',u'\u300F',u'\u2019',u'\u201C',u'\u201D',
        u'\u2018',u'\uFF08',u'\uFF09',u'\u3014',u'\u3015',u'\u2026',u'\u2013',u'\uFF0E',
        u'\u2014',u'\u300A',u'\u300B',u'\u3008',u'\u3009'
    ]
    return c in arr

def remove_space_in_sentence(sentence):
    s = sentence.strip()
    rtn = ''
    for i,c in enumerate(s):
        if c.isspace() and i == len(s)-1:
            continue
        if c.isspace():
            prev_char = rtn[-1] if len(rtn)>0 else ''
            next_char = s[i+1]
            if next_char.isspace():
                continue
            elif is_chinese(next_char) or is_chinese_punctuation(next_char):
                continue
            elif (is_chinese(prev_char) or is_chinese_punctuation(prev_char)) and not is_chinese(next_char):
                continue
            else:
                rtn += c
        else:
            rtn += c
    return rtn
