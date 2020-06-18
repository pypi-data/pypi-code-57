import pytest
from sentence_spliter.spliter_simple import Spliter

def test_cut_to_sentences_zh_1():
    '''
    正常切分,按照句号,感叹号,问号,省略号,分号切分
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!他的手掌轻柔地搁在被告席的桌面上——在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。' \
           '后来,旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    #----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '他的手掌轻柔地搁在被告席的桌面上——在一场对于他的审判中……','这是他所能保持的最为超脱的姿态了。',
                       '后来,旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;','另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_2():
    '''
    双引号内遇到切分符号不切分
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!"他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。"' \
           '后来,旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '"他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。"',
                       '后来,旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;', '另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_3():
    '''
    双引号后遇到逗号不切分,其他情况切分
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!"他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。"' \
           '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '"他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。"',
                       '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_4():
    '''
    括号内遇到切分符号不切分
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).' \
           '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).',
                       '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_5():
    '''
    整个段落只有一个符号
    :return:
    '''
    spliter = Spliter()
    text = '...'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['...']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_6():
    '''
    结束符后面是一个标点符号
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).' \
           '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?!'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).',
                       '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?!']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_zh_7():
    '''
    遇到小数的句号不切分
    :return:
    '''
    spliter = Spliter()
    text = '被告人宫本天道傲然端坐,刻板却不失优雅!(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).' \
           '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?!我买了4.5斤水果.'
    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    # ----正常切分----
    cut_sent_expect = ['被告人宫本天道傲然端坐,刻板却不失优雅!', '(他的手掌轻柔地搁在被告席的桌面上.在一场对于他的审判中……这是他所能保持的最为超脱的姿态了。).',
                       '后来,"旁听席上的一些人认为他的寂默意味着对整个庭审过程的蔑视;",另一些人则坚持他是为了掩盖对即将做出的宣判的恐惧?!','我买了4.5斤水果.']
    assert cut_sent_expect == cut_sents_actual

def test_cut_to_sentences_en_1():
    '''
    正常切分,按照句号,感叹号,问号,省略号,分号切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; recording or otherwise, without the prior written permission of the publisher! Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' recording or otherwise, without the prior written permission of the publisher!''',
                        ''' Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.''']

    assert cut_sents_actual == cut_sents_expect

def test_cut_to_sentences_en_2():
    '''
   括号内遇到切分符号不切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part! of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; recording or otherwise, without the prior written permission of the publisher! Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part! of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' recording or otherwise, without the prior written permission of the publisher!''',
                        ''' Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.''']

    assert cut_sents_actual == cut_sents_expect

def test_cut_to_sentences_en_3():
    '''
    双引号内遇到切分符号不切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; "recording or otherwise. without the prior written permission of the publisher!". Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' "recording or otherwise. without the prior written permission of the publisher!".''',
                        ''' Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.''']

    assert cut_sents_actual == cut_sents_expect

def test_cut_to_sentences_en_4():
    '''
    遇到小数不切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available 5.6 this publication (or any part of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; recording or otherwise, without the prior written permission of the publisher! Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available 5.6 this publication (or any part of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' recording or otherwise, without the prior written permission of the publisher!''',
                        ''' Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.''']

    assert cut_sents_actual == cut_sents_expect

def test_cut_to_sentences_en_5():
    '''
    遇到小数不切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available 5.6 this publication (or any part of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; recording or otherwise, without the prior written permission of the publisher! Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.?'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available 5.6 this publication (or any part of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' recording or otherwise, without the prior written permission of the publisher!''',
                        ''' Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.?''']

    assert cut_sents_actual == cut_sents_expect

def test_cut_to_sentences_en_6():
    '''
    双引号内遇到切分符号不切分
    :return:
    '''
    spliter = Spliter()
    text = '''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form? or by any means including without limitation electronic. digital, optical, mechanical, photocopying, printing; "recording or otherwise. without the prior written permission of the publisher!", Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.'''

    cut_sents_actual = spliter.cut_to_sentences(paragraph=text)
    print(cut_sents_actual)
    cut_sents_expect = ['''You may not copy, distribute, transmit, reproduce or otherwise make available this publication (or any part of it) in any form?''',
                        ''' or by any means including without limitation electronic.''',
                        ''' digital, optical, mechanical, photocopying, printing;''',
                        ''' "recording or otherwise. without the prior written permission of the publisher!", Any person who does any unauthorised act in relation to this publication may be liable to criminal prosecution and civil claims for damages.''']

    assert cut_sents_actual == cut_sents_expect

if __name__ == '__main__':
    test_cut_to_sentences_zh_1()
    test_cut_to_sentences_zh_2()
    test_cut_to_sentences_zh_3()
    test_cut_to_sentences_zh_4()
    test_cut_to_sentences_zh_5()
    test_cut_to_sentences_zh_6()
    test_cut_to_sentences_zh_7()
    test_cut_to_sentences_en_1()
    test_cut_to_sentences_en_2()
    test_cut_to_sentences_en_3()
    test_cut_to_sentences_en_4()
    test_cut_to_sentences_en_5()
    test_cut_to_sentences_en_6()

