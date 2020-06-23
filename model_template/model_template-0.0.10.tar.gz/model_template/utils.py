from tqdm import tqdm
import numpy as np


class GpamTokenizer:
    def __init__(self, vocab, texts):
        self.vocab = vocab
        self.texts = texts
        self.dict_vocab = {}

    def list_2_dict(self):
        id = 1
        for word in self.vocab:
            self.dict_vocab[word] = id
            id += 1

    def return_tokens(self, text):
        return text.split(" ")

    def transform_tokens(self, tokens):
        result_transform = []
        for token in tokens:
            try:
                id = self.dict_vocab[token]
                result_transform.append(id)
            except Exception:
                continue

        return result_transform

    def pad_vector(self, texts, num):
        reshape_v = []

        for each in tqdm(texts):
            if len(each) >= num:
                reshape_v.append(each[0:num])
            else:
                zeros = num - len(each)
                temp = each
                v_zeros = [0 for each in range(zeros)]
                temp.extend(v_zeros)
                reshape_v.append(temp)

        return reshape_v

    def tokenizer_with_vocab(self, num):
        self.list_2_dict()
        result_texts = []
        for i in tqdm(range(len(self.texts))):
            tokens = self.return_tokens(self.texts[i])
            result_transform = self.transform_tokens(tokens)
            result_texts.append(result_transform)

        result = self.pad_vector(result_texts, num)

        return np.matrix(result)


def binarize_pred(preds):
    new_preds = []
    for each in preds:
        num = max(each)
        new_list = np.asarray([0 for temp in range(len(each))])
        new_list[np.where(each == num)[0][0]] = 1
        new_preds.append(np.asarray(new_list))
    return new_preds
