import os
import word2vec
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
import matplotlib
from tools import get_penalty, get_segments
from algorithm import split_optimal, split_greedy, get_total
import sys

def main(book_path):
    corpus_path = './text8'  
    wrdvec_path = 'wrdvecs-text8.bin'

    if not os.path.exists(wrdvec_path):
        word2vec.word2vec(corpus_path, wrdvec_path, cbow=1, iter_=5, hs=1, threads=4, sample='1e-5', window=15, size=200, binary=1)

    model = word2vec.load(wrdvec_path)
    wrdvecs = pd.DataFrame(model.vectors, index=model.vocab)
    del model
    print(wrdvecs.shape)

    nltk.download('punkt')
    sentence_analyzer = nltk.data.load('tokenizers/punkt/english.pickle')

    segment_len = 30  # segment target length in sentences

    with open(book_path, 'rt', encoding="utf8") as f:
        text = f.read().replace('\n', '¤')  # punkt tokenizer handles newlines not so nice

    sentenced_text = sentence_analyzer.tokenize(text)
    vecr = CountVectorizer(vocabulary=wrdvecs.index)

    sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)

    penalty = get_penalty([sentence_vectors], segment_len)
    print('penalty %4.2f' % penalty)

    optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=250)
    segmented_text = get_segments(sentenced_text, optimal_segmentation)

    f = open("segmentaion_result.csv", "w", encoding="utf8")
    f.write("index,text\n")
    seg_count = 0

    for s in segmented_text:
        print("\n===========Start of segment===========\n")
        print(s[:3], "...........", s[-2:-1])
        f.write(str(seg_count)+",")
        for ss in s:
            f.write(re.sub('\W+',' ', ss))
        f.write("\n")    
        print("\n===========End of segment===========\n")
        seg_count += 1

    f.close()

    print('%d sentences, %d segments, avg %4.2f sentences per segment' % (
        len(sentenced_text), len(segmented_text), len(sentenced_text) / len(segmented_text)))

    greedy_segmentation = split_greedy(sentence_vectors, max_splits=len(optimal_segmentation.splits))
    greedy_segmented_text = get_segments(sentenced_text, greedy_segmentation)

    totals = [get_total(sentence_vectors, seg.splits, penalty) 
              for seg in [optimal_segmentation, greedy_segmentation]]
    print('optimal score %4.2f, greedy score %4.2f' % tuple(totals))
    print('ratio of scores %5.4f' % (totals[0] / totals[1]))