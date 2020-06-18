import numpy as np
import torch
from torch.utils.data import Dataset

np.random.seed(12345)


# class DataReader:
#     NEGATIVE_TABLE_SIZE = 1e8
#
#     def __init__(self, inputFileName, min_count):
#
#         # self.negatives = []
#         # self.discards = []
#         self.negpos = 0
#
#         # self.word2id = dict()
#         # self.id2word = dict()
#         self.sentences_count = 0
#         self.token_count = 0
#         # self.word_frequency = dict()
#
#         self.inputFileName = inputFileName
#         # self.read_words(min_count)
#         # self.initTableNegatives()
#         # self.initTableDiscards()
#
#     def read_words(self, min_count):
#         word_frequency = dict()
#         for line in open(self.inputFileName, encoding="utf8"):
#             line = line.split()
#             if len(line) > 1:
#                 self.sentences_count += 1
#                 for word in line:
#                     word = word.split('_')[0]
#                     if len(word) > 0:
#                         self.token_count += 1
#                         word_frequency[word] = word_frequency.get(word, 0) + 1
#
#                         if self.token_count % 1000000 == 0:
#                             print("Read " + str(int(self.token_count / 1000000)) + "M words.")
#
#         wid = 0
#         for w, c in word_frequency.items():
#             if c < min_count:
#                 continue
#             self.word2id[w] = wid
#             self.id2word[wid] = w
#             self.word_frequency[wid] = c
#             wid += 1
#         print("Total embeddings: " + str(len(self.word2id)))
#
#     def initTableDiscards(self):
#         t = 0.0001
#         f = np.array(list(self.word_frequency.values())) / self.token_count
#         self.discards = np.sqrt(t / f) + (t / f)
#
#     def initTableNegatives(self):
#         pow_frequency = np.array(list(self.word_frequency.values())) ** 0.5
#         words_pow = sum(pow_frequency)
#         ratio = pow_frequency / words_pow
#         count = np.round(ratio * DataReader.NEGATIVE_TABLE_SIZE)
#         for wid, c in enumerate(count):
#             self.negatives += [wid] * int(c)
#         self.negatives = np.array(self.negatives)
#         np.random.shuffle(self.negatives)
#
#     def getNegatives(self, target, size):  # TODO check equality with target
#         response = self.negatives[self.negpos:self.negpos + size]
#         self.negpos = (self.negpos + size) % len(self.negatives)
#         if len(response) != size:
#             return np.concatenate((response, self.negatives[0:self.negpos]))
#         return response


# -----------------------------------------------------------------------------------------------------------------

class Word2vecDataset(Dataset):
    def __init__(self, inputFileName, side_num = 0, neg_num = 5, sentences_count = 1000000):
        # self.data = data
        # self.window_size = window_size
        self.sentences_count = sentences_count
        self.neg_num = neg_num
        self.side_num = side_num
        self.input_file = open(inputFileName, encoding="utf8")

    def __len__(self):
        return self.sentences_count

    def __getitem__(self, idx):
        while True:
            line = self.input_file.readline()
            if not line:
                self.input_file.seek(0, 0)
                line = self.input_file.readline()

            if len(line) > 1:
                words = line.split(' ')
                assert len(words) == self.neg_num+2
                assert len(words[0].split('_')) == self.side_num
                return [words[0],words[1],words[2:]]

    @staticmethod
    def collate(batches):
        all_u = [u for batch in batches for u, _, _ in batch if len(batch) > 0]
        all_u = [list(map(int,x.split('_'))) for x in all_u]
        all_v = [v for batch in batches for _, v, _ in batch if len(batch) > 0]
        all_v = [list(map(int,x.split('_'))) for x in all_v]
        all_neg_v = [neg_v for batch in batches for _, _, neg_v in batch if len(batch) > 0]
        all_neg_v = [[list(map(int,x.split('_'))) for x in xx] for xx in all_neg_v]

        return torch.LongTensor(all_u), torch.LongTensor(all_v), torch.LongTensor(all_neg_v)
