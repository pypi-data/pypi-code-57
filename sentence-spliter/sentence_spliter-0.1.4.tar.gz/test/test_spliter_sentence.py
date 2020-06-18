from sentence_spliter.spliter_sentence import Spliter

def test_cut_to_sentences_en():
    options = {
            'language': 'en',
            'long_short_sent_handle': False,
            'max_length': 150,
            'min_length': 15,
            'hard_max_length': 300,
            'remove_blank': False
        }
    spliter = Spliter(**options)
    text = 'Hello world.kkkkk!'
    cut_sent_actual = spliter.cut_to_sentences(text=text)
    print(cut_sent_actual)
    cut_sent_expect = ['''Hello world.''','''kkkkk!''']
    assert cut_sent_expect == cut_sent_actual

def test_cut_to_sentences_zh_1():
    '''
    短句合并
    :return:
    '''
    options = {
        'language': 'zh',
        'long_short_sent_handle': True,
        'max_length': 20,
        'min_length': 5,
        'hard_max_length': 22,
        'remove_blank': True
    }
    spliter = Spliter(**options)

    text = '旁听席.座无虚席,但法庭里并未显现出乡间谋杀.'

    cut_sent_actual = spliter.cut_to_sentences(text=text)
    print(cut_sent_actual)
    cut_sent_expect = ['旁听席.座无虚席,','但法庭里并未显现出乡间谋杀.']
    assert cut_sent_expect == cut_sent_actual

def test_cut_to_sentences_zh_2():
    '''
    长句切开
    :return:
    '''
    options = {
        'language': 'zh',
        'long_short_sent_handle': True,
        'max_length': 20,
        'min_length': 5,
        'hard_max_length': 22,
        'remove_blank': True
    }
    spliter = Spliter(**options)
    text = '旁听席，座无虚席,但法庭里并未显现出乡间谋杀案庭审过程中常见的狂欢氛围。'
    cut_sent_actual = spliter.cut_to_sentences(text=text)
    print(cut_sent_actual)
    cut_sent_expect = ['旁听席，座无虚席,', '但法庭里并未显现出乡间谋杀案庭审过程中常见的', '狂欢氛围。']
    assert cut_sent_expect == cut_sent_actual

def test_cut_to_sentences_zh_3():
    '''
    长句切开
    :return:
    '''
    options = {
        'language': 'zh',
        'long_short_sent_handle': True,
        'max_length': 20,
        'min_length': 5,
        'hard_max_length': 22,
        'remove_blank': True
    }
    spliter = Spliter(**options)
    text = '但法庭里并未显现出乡间谋杀案庭审过程中常见的狂欢氛围。'
    cut_sent_actual = spliter.cut_to_sentences(text=text)
    print(cut_sent_actual)
    cut_sent_expect = ['但法庭里并未显现出乡间谋杀案庭审过程中常见的', '狂欢氛围。']
    assert cut_sent_expect == cut_sent_actual

def test_cut_to_sentences_zh_4():
    '''
    连着两个长句切开
    :return:
    '''
    options = {
        'language': 'zh',
        'long_short_sent_handle': True,
        'max_length': 15,
        'min_length': 5,
        'hard_max_length': 20,
        'remove_blank': True
    }
    spliter = Spliter(**options)
    text = '我看着镜子里的自己,我知道我受洗时的名字叫克莱门汀.所以如果大伙儿管我叫克莱门，想想看就算是叫我克莱门汀.'
    cut_sent_actual = spliter.cut_to_sentences(text=text)
    print(cut_sent_actual)
    # cut_sent_expect = ['但法庭里并未显现出乡间谋杀案庭审过程中常见的', '狂欢氛围。']
    # assert cut_sent_expect == cut_sent_actual

def test_cut_sentences_book():
    options = {
        'language': 'zh',
        'long_short_sent_handle': True,
        'max_length': 150,
        'min_length': 15,
        'hard_max_length': 300,
        'remove_blank': True
    }
    spliter = Spliter(**options)
    with open('./data/005-假如比尔街可以作证-zh.txt','r',encoding='utf-8') as f:
        sentence = f.read()
    output_lines = []
    output_lines.extend(spliter.cut_to_sentences(sentence))
    output_path = './data/005-假如比尔街可以作证-zh-cut.txt'
    open(output_path, 'w', encoding='utf-8').write('\n'.join(output_lines))

    #---判断每条句子的长度----
    with open(output_path,'r',encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        if len(line) < options['min_length'] or len(line) < options['max_length']:
            assert Exception('error')


if __name__ == '__main__':
    test_cut_to_sentences_en()
    test_cut_to_sentences_zh_1()
    test_cut_to_sentences_zh_2()
    test_cut_to_sentences_zh_3()
    test_cut_sentences_book()
    test_cut_to_sentences_zh_4()
