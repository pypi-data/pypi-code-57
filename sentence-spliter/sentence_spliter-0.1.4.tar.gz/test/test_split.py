from sentence_spliter import split
from sentence_spliter.spliter_sentence import Spliter

# -- case 1 -- #
sentence = '锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦.'
out = split(sentence)

# # -- case 2 import option dict -- #
# option = {
#     'language': 'zh',  # 'zh' chinese, 'en' english
#     'long_short_sent_handle': True,  # 'y'自然切分，不处理长短句；'n'处理长短句
#     'max_length': 120,  # 最长句子，默认值150
#     'min_length': 15,  # 最短句子，默认值15
#     'hard_max_length': 120,  # 强制截断，默认值300
#     'remove_blank': True  # 是否要我删除句子中的空白
# }
# #out = split(sentence, option)
#
# # -- case 3 change some of opts -- #
# #out = split(sentence, min_length=5)
#
# # -- case 4 build obj -- #
# splter = Spliter(**option)
# splter.cut_to_sentences(sentence)

print(out)
