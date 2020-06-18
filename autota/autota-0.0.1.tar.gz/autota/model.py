import re
from textrank4zh import TextRank4Keyword
# from .rake import *
# import pandas as pd
# import numpy as np
# from .util import PDFProcessor
# from scipy.spatial.distance import cosine
# from bert_serving.client import BertClient
# import math
# import jieba
# import requests
# from difflib import SequenceMatcher 


class TextRank:
    def __init__(self, n_word, word_min_len, sentence_min_len):
        self.n_word = n_word
        self.word_min_len = word_min_len
        self.sentence_min_len = sentence_min_len

    def get_keywords(self, text):
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=text, lower=True, window=2) 
        kw_list = []
        for item in tr4w.get_keywords(self.n_word, word_min_len=self.word_min_len):
            kw_list.append(item.word)
        return kw_list

    def get_key_sentences(self, kw_list, text):
        text_list = re.split(',|。',text)
        sentence_list = list(filter(lambda x: len(x) > self.sentence_min_len, text_list))
        sentence_set = set(sentence_list)
        sentence_dict = {s:0 for s in list(sentence_set)}
        for word in kw_list:
            for sentence, occ in sentence_dict.items():
                if word in sentence:
                    sentence_dict[sentence] += 1
        important_sentece = {k:v for k, v in sentence_dict.items() if v != 0}
        return important_sentece

# class Rake:
#     def __init__(self, n_word, sentence_min_len):
#         self.n_word = n_word
#         self.sentence_min_len = sentence_min_len

#     def get_keywords(self, text):
#         kw_tuple = run(text)
#         kw_list = [word for (word, weight) in kw_tuple]
#         return kw_list[:self.n_word]

#     def get_key_sentences(self, kw_list, text):
#         text_list = re.split(',|。',text)
#         sentence_list = list(filter(lambda x: len(x) > self.sentence_min_len, text_list))
#         sentence_set = set(sentence_list)
#         sentence_dict = {s:0 for s in list(sentence_set)}
#         for word in kw_list:
#             for sentence, occ in sentence_dict.items():
#                 if word in sentence:
#                     sentence_dict[sentence] += 1
#         important_sentece = {k:v for k, v in sentence_dict.items() if v != 0}
#         return important_sentece

# class BertSum:
#     def __init__(self, ratio, article):
#         self.model = BertClient(ip="140.115.53.158", port=5555)
#         self.ratio = ratio
#         self.article = article
#         self.concept = self.model.encode(list(self.article))[0]
#         sentence_cnt = 0
#         page_content = article.split('。')
#         if '' in page_content:
#             page_content.remove('')
#         for page in page_content:
#             sentences = page.split(',')
#             if '' in sentences:
#                 sentences.remove('')
#             for s in sentences:
#                 sentence_cnt += 1
#         self.num_sentence = math.ceil(sentence_cnt*self.ratio)
    
#     def get_key_sentences(self):
#         distance = {}
#         page_content = self.article.split('。')
#         if '' in page_content:page_content.remove('')
#         for page in page_content:
#             sentences = page.split(',')
#             if '' in sentences:sentences.remove('')
#             for s in sentences:
#                 embedding = self.model.encode(list(s))[0]
#                 distance.update({s: self.get_distance(self.concept, embedding)})
#         sort_dict = {k: v for k, v in sorted(distance.items(), key=lambda item: item[1])}
#         dict_slice = lambda adict, start, end: { k:adict[k] for k in list(adict.keys())[start:end]}
#         return dict_slice(sort_dict, 0, self.num_sentence)

#     def get_distance(self, p1, p2):
#         return cosine(p1, p2)

# class BertForEmbedding:
#     def __init__(self):
#         self.model = BertClient(ip="140.115.53.158", port=5555)
    
#     def embed_slide(self, slide_path):
#         pdf = PDFProcessor(slide_path)
#         page_centrals = []
#         for i in range(pdf.pageCount):
#             text_list = pdf.get_page_text(i+1)
#             text = '。'.join(text_list)
#             if text != '':
#                 page_central = self.model.encode([text])
#             else:
#                 page_central = np.zeros((1, 768))
#             page_centrals.append(page_central)
#         return page_centrals
#     def embed_text(self, text):
#         if text != '':
#             embedding = self.model.encode([text])
#         else:
#             embedding = np.zeros((1, 768))
#         return embedding

# class MemoFeaturesExtractor:
#     def __init__(self, content_embedding, slide_raw_text, slide_kw_list):
#         self.content_embedding = content_embedding
#         self.slide_raw_text = slide_raw_text
#         self.slide_kw_list = slide_kw_list
#         # jieba.enable_paddle()

#     def get_length(self, memo_text):
#         memo_text = memo_text.replace(";:::sgquotation:::;", "'").replace(";:::dbquotation:::;", "\'\'").replace(";:::nl:::;", "\n")
#         # tokenizer = hanlp.utils.rules.tokenize_english
#         # length = len(tokenizer(memo_text))
#         # if length <= 1:
#         #     #處理中文
#         return len(memo_text)
#     def get_lcs(self, memo_text):
#         memo_text = memo_text.replace(";:::sgquotation:::;", "'").replace(";:::dbquotation:::;", "\'\'").replace(";:::nl:::;", "\n")
#         seqMatch = SequenceMatcher(None, self.slide_raw_text, memo_text)
#         match = seqMatch.find_longest_match(0, len(self.slide_raw_text), 0, len(memo_text))

#         return match.size
#     def get_semantic_similarity(self, memo, page_no):
#         model = BertForEmbedding()
#         memo_embedding = model.embed_text(memo)[0]
#         # spec_page_text = self.slide_page_text[page_no - 1]
#         # url = 'http://140.115.53.158:5000/embedding' #call API
#         # model = BertForEmbedding(model_path='../model')
#         page_central = self.content_embedding[page_no - 1]
#         cos_sim = 1 - cosine(page_central[0], memo_embedding) / 2
        
#         return cos_sim
#     def get_kw_ratio(self, memo_text):
#         memo_text = memo_text.replace(";:::sgquotation:::;", "'").replace(";:::dbquotation:::;", "\'\'").replace(";:::nl:::;", "\n")
#         tokens = jieba.cut(memo_text)
#         hit_kw = list(set(tokens).intersection(set(self.slide_kw_list)))
#         return 0.8 + len(hit_kw) / len(self.slide_kw_list)

# class BertForGuiding:
#     def __init__(self, model_path):
#         # self.use_cuda = use_cuda

#         self.model = BertClient(ip="140.115.53.158", port=5555)
#         # if self.use_cuda:
#         #     device = torch.device('cuda')
#         #     self.model.to(device)
#         # else:
#         #     device = torch.device('cpu')
#         #     self.model.to(device)

#     def get_central(self, pdf):
#         page_central = []
#         for i in range(pdf.pageCount):
#             text = ','.join(pdf.get_page_text(i+1))
# #     for token in pdf.get_page_text(i + 1):
#             feature = self.model.encode([text])
#             page_central.append(feature)
#         return page_central
        
#     def get_ans_feature(self, ans):
#         ans_feature = self.model.encode([ans])
#         return ans_feature

#     def get_distance(self, ans_feature, centrals):
#         index = 0
#         distance_array = []
#         for pc in centrals:
#             distance_array.append((index + 1, cosine(pc.numpy(), ans_feature.numpy())))
#         return distance_array

# class GPT2ForQuestionGeneration:
#     def __init__(self):
#         self.api_url = 'http://140.115.53.158:9527/generate'
    
#     def generate(self, sentence):
#         params = {'sentence': sentence}
#         resp = requests.get(self.api_url, params=params)
#         data = dict(resp.json())['data']
#         questions = []
#         for d in data:
#             questions.append(d["question"])
#         return questions