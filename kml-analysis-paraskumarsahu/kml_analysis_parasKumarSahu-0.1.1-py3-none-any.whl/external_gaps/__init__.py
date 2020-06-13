import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk

def lemmatize_stemming(text):
	stemmer = PorterStemmer()
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


def run(file_name, word_vector_model):
	start_segmentation(file_name, word_vector_model)
	data = pd.read_csv('segmentaion_result.csv', error_bad_lines=False, encoding="utf8")
	data_text = data[['text']]
	data_text['index'] = data_text.index
	documents = data_text

	print(len(documents), "Documents found")

	np.random.seed(2018)

	nltk.download('wordnet')

	print(WordNetLemmatizer().lemmatize('went', pos='v'))

	stemmer = SnowballStemmer('english')

	processed_docs = documents['text'].map(preprocess)

	dictionary = gensim.corpora.Dictionary(processed_docs)

	bow_corpus = 0
	if(len(dictionary) != 0):
		bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
	else:
		print("Change filter values to run!")
		exit()

	lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=len(documents), id2word=dictionary, passes=2, workers=4)


	for idx, topic in lda_model.print_topics(-1):
	    print('Topic: {} \n======\nWords: {}'.format(idx, topic))

	M = []
	count = 0
	for bow_doc in bow_corpus:
		M_r = [0]*len(documents)
		for index, score in sorted(lda_model[bow_doc], key=lambda tup: -1*tup[1]):
			M_r[index] = score
		M.append(M_r)
		count += 1

	print("External Knowledge Gaps:-")

	f = open("external_gaps.txt", "w")
	f.write(str(pd.DataFrame(M)))
	no_gaps = 0
	threshold = 1.75

	for i in range(len(M)-1):
		tmp_sum = 0	
		for j in range(len(M[0])):
			tmp_sum += abs(M[i+1][j]-M[i][j])
		if tmp_sum > threshold:
			no_gaps += 1	
			print("Gap found between segments", i+1, "and", i+2)
			f.write("Gap found between segments "+str(i+1)+" and "+str(i+2)+"\n")

	print("Total", no_gaps, "Knowledge-gaps found!")
	f.write("Total "+str(no_gaps)+" Knowledge-gaps found!\n")

####################################################################################################################################
import os
import word2vec
from sklearn.feature_extraction.text import CountVectorizer
import re
import sys

def start_segmentation(book_path, word_vector_model):
    model = word2vec.load(word_vector_model)
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

#########################################################################################################################################
import random
from numpy.linalg import norm
from collections import namedtuple
Segmentation = namedtuple('Segmentation', 'total splits gains min_gain optimal')

def get_segments(text_particles, segmentation):
    segmented_text = []
    L = len(text_particles)
    for beg, end in zip([0] + segmentation.splits, segmentation.splits + [L]):
        segmented_text.append(text_particles[beg:end])
    return segmented_text

def get_penalty(docmats, segment_len):
    penalties = []
    for docmat in docmats:
        avg_n_seg = docmat.shape[0] / segment_len
        max_splits = int(avg_n_seg) + (random.random() < avg_n_seg % 1) - 1
        if max_splits >= 1:
            seg = split_greedy(docmat, max_splits=max_splits)
            if seg.min_gain < np.inf:
                penalties.append(seg.min_gain)
    if len(penalties) > 0:
        return np.mean(penalties)
    raise ValueError('All documents too short for given segment_len.')


def P_k(splits_ref, splits_hyp, N):
    k = round(N / (len(splits_ref) + 1) / 2 - 1)
    ref = np.array(splits_ref, dtype=np.int32)
    hyp = np.array(splits_hyp, dtype=np.int32)

    def is_split_between(splits, l, r):
        return np.sometrue(np.logical_and(splits - l >= 0, splits - r < 0))

    acc = 0
    for i in range(N-k):
        acc += is_split_between(ref, i, i+k) != is_split_between(hyp, i, i+k)

    return acc / (N-k)

#########################################################################################################################################

def split_greedy(docmat, penalty=None, max_splits=None):
    L, dim = docmat.shape

    assert max_splits is not None or (penalty is not None and penalty > 0)

    # norm(cumvecs[j] - cumvecs[i]) == norm(w_i + ... + w_{j-1})
    cumvecs = np.cumsum(np.vstack((np.zeros((1, dim)), docmat)), axis=0)

    # cut[0] seg[0] cut[1] seg[1] ... seg[L-1] cut[L]
    cuts = [0, L]
    segscore = dict()
    segscore[0] = norm(cumvecs[L, :] - cumvecs[0, :], ord=2)
    segscore[L] = 0     # corner case, always 0
    score_l = norm(cumvecs[:L, :] - cumvecs[0, :], axis=1, ord=2)
    score_r = norm(cumvecs[L, :] - cumvecs[:L, :], axis=1, ord=2)
    score_out = np.zeros(L)
    score_out[0] = -np.inf  # forbidden split position
    score = score_out + score_l + score_r

    min_gain = np.inf
    while True:
        split = np.argmax(score)

        if score[split] == - np.inf:
            break

        cut_l = max([c for c in cuts if c < split])
        cut_r = min([c for c in cuts if split < c])
        split_gain = score_l[split] + score_r[split] - segscore[cut_l]
        if penalty is not None:
            if split_gain < penalty:
                break

        min_gain = min(min_gain, split_gain)

        segscore[cut_l] = score_l[split]
        segscore[split] = score_r[split]

        cuts.append(split)
        cuts = sorted(cuts)

        if max_splits is not None:
            if len(cuts) >= max_splits + 2:
                break

        # differential changes to score arrays
        score_l[split:cut_r] = norm(
            cumvecs[split:cut_r, :] - cumvecs[split, :], axis=1, ord=2)
        score_r[cut_l:split] = norm(
            cumvecs[split, :] - cumvecs[cut_l:split, :], axis=1, ord=2)

        # adding following constant not necessary, only for score semantics
        score_out += split_gain
        score_out[cut_l:split] += segscore[split] - split_gain
        score_out[split:cut_r] += segscore[cut_l] - split_gain
        score_out[split] = -np.inf

        # update score
        score = score_out + score_l + score_r

    cuts = sorted(cuts)
    splits = cuts[1:-1]
    if penalty is None:
        total = None
    else:
        total = sum(
            norm(cumvecs[l, :] - cumvecs[r, :], ord=2)
            for l, r in zip(cuts[: -1], cuts[1:])) - len(splits) * penalty
    gains = []
    for beg, cen, end in zip(cuts[:-2], cuts[1:-1], cuts[2:]):
        no_split_score = norm(cumvecs[end, :] - cumvecs[beg, :], ord=2)
        gains.append(segscore[beg] + segscore[cen] - no_split_score)

    return Segmentation(total, splits, gains,
                        min_gain=min_gain, optimal=None)


def split_optimal(docmat, penalty, seg_limit=None):
    L, dim = docmat.shape
    lim = L if seg_limit is None else seg_limit
    assert lim > 0
    assert penalty > 0

    acc = np.full((L, lim), -np.inf, dtype=np.float32)
    colmax = np.full((L,), -np.inf, dtype=np.float32)
    ptr = np.zeros(L, dtype=np.int32)

    for i in range(L):
        score_so_far = colmax[i-1] if i > 0 else 0.

        ctxvecs = np.cumsum(docmat[i:i+lim, :], axis=0)
        winsz = ctxvecs.shape[0]
        score = norm(ctxvecs, axis=1, ord=2)
        acc[i, :winsz] = score_so_far - penalty + score

        deltas = np.where(acc[i, :winsz] > colmax[i:i+lim])[0]
        js = i + deltas
        colmax[js] = acc[i, deltas]
        ptr[js] = i

    path = [ptr[-1]]
    while path[0] != 0:
        path.insert(0, ptr[path[0] - 1])

    splits = path[1:]
    gains = get_gains(docmat, path[1:])
    optimal = all(np.diff([0] + splits + [L]) < lim)

    total = colmax[-1] + penalty

    return Segmentation(total, splits, gains,
                        min_gain=None, optimal=optimal)


def get_total(docmat, splits, penalty):
    L, dim = docmat.shape
    cuts = [0] + list(splits) + [L]
    cumvecs = np.cumsum(np.vstack((np.zeros((1, dim)), docmat)), axis=0)
    return sum(
        norm(cumvecs[l, :] - cumvecs[r, :], ord=2)
        for l, r in zip(cuts[:-1], cuts[1:])) - len(splits) * penalty


def get_gains(docmat, splits, width=None):
    gains = []
    L = docmat.shape[0]
    for beg, cen, end in zip([0] + splits[:-1], splits, splits[1:] + [L]):
        if width is not None and width > 0:
            beg, end = max(cen - width, 0), min(cen + width, L)

        slice_l, slice_r, slice_t = [slice(beg, cen),
                                     slice(cen, end),
                                     slice(beg, end)]

        gains.append(norm(docmat[slice_l, :].sum(axis=0), ord=2) +
                     norm(docmat[slice_r, :].sum(axis=0), ord=2) -
                     norm(docmat[slice_t, :].sum(axis=0), ord=2))
    return gains
