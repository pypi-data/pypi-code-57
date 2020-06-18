from sentence_spliter.spliter_sentence import Spliter
option_default = {
    'language': 'zh',  # 'zh' chinese, 'en' english
    'long_short_sent_handle': True,  # False自然切分，不处理长短句；True处理长短句
    'max_length': 120,  # 最长句子，默认值150
    'min_length': 15,  # 最短句子，默认值15
    'hard_max_length': 120,  # 强制截断，默认值300
    'remove_blank': True  # 是否要我删除句子中的空白
}

__spliter = Spliter(**option_default)
split = __spliter.cut_to_sentences

# def split_by_opt(str_block, option=option_default) -> [str]:
#     spliter = Spliter(**option)
#     return spliter.cut_to_sentences(str_block)
#
#
# def split(str_block,
#           language='zh',
#           long_short_sent_handle=True,
#           max_length=150,
#           min_length=15,
#           hard_max_length=120,
#           remove_blank=True):
#     spliter = Spliter(language=language,
#                       long_short_sent_handle=long_short_sent_handle,
#                       max_length=max_length,
#                       min_length=min_length,
#                       hard_max_length=hard_max_length,
#                       remove_blank=remove_blank)
#     return spliter.cut_to_sentences(str_block)
