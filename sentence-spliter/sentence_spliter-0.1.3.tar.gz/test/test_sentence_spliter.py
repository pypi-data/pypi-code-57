# from sentence_spliter.sentence_spliter import Spliter
from sentence_spliter.spliter_sentence import Spliter
from loguru import logger
import json

def test_spliter():
    options = {
        'language': 'zh',
        'long_short_sent_handle':'y',
        'hard_max_length': 300,
        'max_length': 150,
        'min_length': 15,
        'remove_blank':'True'
    }
    spliter = Spliter(options)
    input_path = '../test/data/test.txt'
    output_path = '../test/data/cut_sentences.txt'
    with open(input_path,'r',encoding='utf-8') as f_read:
        sentence = f_read.read()
    logger.debug(sentence)
    output_lines = []
    output_lines.extend(spliter.cut_to_sentences(sentence))
    open(output_path, 'w', encoding='utf-8').write('\n'.join(output_lines))


def test_spliter1():
    options_zh = {
        'language': 'zh',
        'long_short_sent_handle':'y',
        'hard_max_length': 300,
        'max_length': 150,
        'min_length': 15,
        'remove_blank':'True'
    }
    options_en = {
        'language': 'en',
        'long_short_sent_handle': 'n',
        'hard_max_length': 300,
        'max_length': 150,
        'min_length': 15,
        'remove_blank': 'True'
    }
    with open('linguee-32.json', 'r', encoding='utf-8') as f_read:
        for i, each_data in enumerate(f_read):
            each_data = json.loads(each_data)
            spliter_zh = Spliter(options_zh)
            spliter_en = Spliter(options_en)

            spliter_zh.cut_to_sentences(text=each_data['zh'])

            spliter_en.cut_to_sentences(text=each_data['en'])


if __name__ == '__main__':
    test_spliter1()

