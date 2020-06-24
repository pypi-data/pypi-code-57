import math
import unicodedata


def sen_tokenizer(text: str, split_set="。!?！？"):
    sen = []
    sen_ind = 0
    for i, cs in enumerate(text):
        if cs in split_set:
            sen.append(cs)
            if len("".join(sen).strip()) > 1:
                yield sen, sen_ind, len(sen)
            # yield sen, sen_ind, len(sen)
            sen = []
            sen_ind = i + 1
        else:
            sen.append(cs)
    else:
        if len("".join(sen).strip()) > 1:
            yield sen, sen_ind, len(sen)


def min_len_sen_tokenizer(text: str, split_set="。!?！？", minlen=128):
    """
    句子切分， 同时设置切分长度， 当单句过长时进行分割
    :param text:
    :param split_set:
    :param minlen:
    :return:
    """
    for sen_s in sen_tokenizer(text, split_set):
        sen_text, sen_ind, sen_len = sen_s
        if len(sen_text) < minlen:
            yield sen_s, sen_ind, sen_len
        else:
            # 次数
            subnub = math.ceil(len(sen_text) / minlen)
            # 每次的长度
            step = math.ceil(len(sen_text)/subnub)
            for i in range(0, len(sen_text), step):
                sub_sen_text = sen_text[i: i+step]
                sub_sen_len = len(sub_sen_text)
                sub_sen_ind = sen_ind + i
                yield sub_sen_text, sub_sen_ind, sub_sen_len



SEP = "[SEP]"

def is_whitespace(char):
  """Checks whether `chars` is a whitespace character."""
  # \t, \n, and \r are technically contorl characters but we treat them
  # as whitespace since they are generally considered as such.
  if char == " " or char == "\t" or char == "\n" or char == "\r":
    return True
  cat = unicodedata.category(char)
  if cat == "Zs":
    return True
  return False


def is_control(char):
  """Checks whether `chars` is a control character."""
  # These are technically control characters but we count them as whitespace
  # characters.
  if char == "\t" or char == "\n" or char == "\r":
    return False
  cat = unicodedata.category(char)
  if cat in ("Cc", "Cf"):
    return True
  return False


def clean_text(text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
        cp = ord(char)
        if cp == 0 or cp == 0xfffd or is_control(char):
            continue
        if is_whitespace(char):
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def is_chinese_char(cp):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True
    return False


def tokenize_chinese_chars(text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
        cp = ord(char)
        if is_chinese_char(cp):
            output.append(" ")
            output.append(char)
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def whitespace_tokenize(text):
  """Runs basic whitespace cleaning and splitting on a piece of text."""
  text = text.strip()
  if not text:
    return []
  tokens = text.split()
  return tokens


def tokenize(text):
    text = clean_text(text)
    tks = tokenize_chinese_chars(text)
    return whitespace_tokenize(tks)



