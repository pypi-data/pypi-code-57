import unittest
from sentence_spliter.spliter_sentence import Spliter
from sentence_spliter import split

class TestSpilter(unittest.TestCase):

    def test_spliter(self):
        options = {
            'language': 'zh',  # 'zh'中文 'en' 英文
            'long_short_sent_handle': 'y',  # 'y'自然切分，不处理长短句；'n'处理长短句
            'max_length': 150,  # 最长句子，默认值150
            'min_length': 15,  # 最短句子，默认值15
            'hard_max_length': 300,  # 强制截断，默认值300
            'remove_blank': True
        }
        sentence = '你好,我是王丽.我在上海工作.'
        spliter = Spliter(options)
        actual = spliter.cut_to_sentences(sentence)
        expect = ['你好,我是王丽.我在上海工作.']
        self.assertEqual(actual, expect)
        # --- #
        options = {
            'language': 'zh',  # 'zh'中文 'en' 英文
            'long_short_sent_handle': 'y',  # 'y'自然切分，不处理长短句；'n'处理长短句
            'max_length': 13,  # 最长句子，默认值150
            'min_length': 5,  # 最短句子，默认值15
            'hard_max_length': 6,  # 强制截断，默认值300
            'remove_blank': True
        }
        sentence = '锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦.'
        spliter = Spliter(options)
        actual = spliter.cut_to_sentences(sentence)
        expect =['锄禾日当午,汗滴禾下土.','谁知盘中餐,粒粒皆辛苦.']

        #sentence = '你好,啦啦啦啦,哈哈哈哈,呵呵哈哈哈或或或或或或或或或或或或.'
        spliter = Spliter(options)
        actual = spliter.cut_to_sentences(sentence)
        self.assertEqual(actual, expect)
        # ---- #
        options = {
            'language': 'zh',  # 'zh'中文 'en' 英文
            'long_short_sent_handle': 'y',  # 'y'自然切分，不处理长短句；'n'处理长短句
            'max_length': 13,  # 最长句子，默认值150
            'min_length': 5,  # 最短句子，默认值15
            'hard_max_length': 6,  # 强制截断，默认值300
            'remove_blank': True
        }
        sentence = '...'
        spliter = Spliter(options)
        expect = ['...']
        spliter = Spliter(options)
        actual = spliter.cut_to_sentences(sentence)
        self.assertEqual(actual, expect)

    def test_split(self):
        sentence = '锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦.'
        options = {
            'language': 'zh',  # 'zh'中文 'en' 英文
            'long_short_sent_handle': 'y',  # 'y'自然切分，不处理长短句；'n'处理长短句
            'max_length': 13,  # 最长句子，默认值150
            'min_length': 5,  # 最短句子，默认值15
            'hard_max_length': 6,  # 强制截断，默认值300
            'remove_blank': True
        }
        out = split(sentence, options)
        expect = ['锄禾日当午,汗滴禾下土.','谁知盘中餐,粒粒皆辛苦.']
        self.assertEqual(out,expect)

if __name__ == '__main__':
    unittest.main()