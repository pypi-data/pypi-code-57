def read_vocab(vocab_dir):
    """读取词汇表"""
    with open(vocab_dir, "r", encoding="utf-8") as fp:
        words = [_.strip() for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_vec_file(filename):
    chars = []
    vecs = []
    f = open(filename, "r", encoding="utf-8")
    lines = [line.rstrip() for line in f.readlines()]
    for line in lines:
        char, vec = line.split("\t")
        chars.append(char)
        vecs.append(vec.split(" "))
    return chars, vecs


def word_to_vocab_id(s, word_to_id, max_length):
    ids = []
    for char in s:
        try:
            ids.append(word_to_id[char])
        except:
            ids.append(word_to_id["<UNK>"])
    assert len(ids) == len(s)
    if len(ids) >= max_length:
        ids = ids[:max_length]
    else:
        ids = ids + [word_to_id["<PAD>"]] * (max_length - len(ids))
    return ids
