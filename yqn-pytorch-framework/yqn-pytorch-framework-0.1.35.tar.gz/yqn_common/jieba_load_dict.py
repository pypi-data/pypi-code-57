import csv
import re

import jieba


def get_jieba_tokenizer(user_dict_path):
    jieba_tokenizer_name = jieba.Tokenizer()
    # jieba.initialize()
    dics = csv.reader(open(user_dict_path, 'r', encoding='utf8'))
    print("load jieba once ")
    for row in dics:
        if len(row) == 2:
            line = row[0]
            line = re.sub(r'[ ]+', '', str(line))
            line = re.sub("＆", '&', re.sub('）', ')', re.sub('（', '(', line)))
            line = re.sub("：", ":", line)
            line1 = re.sub("\✤+|'|’|;|\xa0|\s|\t|\n|' '|✣|,|，|◇|\.|\x7f|\)|\(|:", '', line)
            if len(line) >= 4:
                line1 = line1
            else:
                line1 = line
            # jieba.add_word(line.strip().upper(), tag=row[1].strip())
            # jieba.suggest_freq(line.strip())
            # jieba.add_word(line1.strip().upper(), tag=row[1].strip())
            # jieba.suggest_freq(line1.strip())
            jieba_tokenizer_name.add_word(line.strip().upper(), tag=row[1].strip())
            jieba_tokenizer_name.suggest_freq(line.strip())
            jieba_tokenizer_name.add_word(line1.strip().upper(), tag=row[1].strip())
            jieba_tokenizer_name.suggest_freq(line1.strip())
            jieba_tokenizer_name.add_word(line1.strip().upper() + ":", tag=row[1].strip())
            jieba_tokenizer_name.suggest_freq(line1.strip())


    return jieba_tokenizer_name

def get_jieba_tokenizer_file(user_dict_path):
    jieba_tokenizer_name = jieba.Tokenizer()
    # jieba.initialize()
    jieba_tokenizer_name.load_userdict(user_dict_path)
    return jieba_tokenizer_name