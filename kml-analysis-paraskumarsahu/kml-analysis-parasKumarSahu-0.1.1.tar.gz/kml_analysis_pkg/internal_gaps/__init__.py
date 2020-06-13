import warnings
warnings.filterwarnings("ignore")

from datetime import datetime 
import os
import pandas as pd
import numpy as np
import re
import nltk
import sys

#For Text Segmentation
import word2vec
from sklearn.feature_extraction.text import CountVectorizer

#For Finding External Gaps
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

#For Readability Measures
import textstat
from scipy.stats import variation

#For Edits and Bytes Info
import requests
from bs4 import BeautifulSoup



def lemmatize_stemming(text):
	stemmer = PorterStemmer()
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


def run(input_folder_path, word_vector_model):
	#Setup	
	startTime = datetime.now()
	folder_name = input_folder_path

	model = word2vec.load(word_vector_model)
	wrdvecs = pd.DataFrame(model.vectors, index=model.vocab)
	del model
	#print(wrdvecs.shape)

	nltk.download('punkt')
	sentence_analyzer = nltk.data.load('tokenizers/punkt/english.pickle')

	segment_len = 30  # segment target length in sentences

	nltk.download('wordnet')

	#Code For Text Segmentation

	f_out = open("Output/"+folder_name+".txt", "w")

	for filename in os.listdir("Input/"+folder_name):
		with open("Input/"+folder_name+"/"+filename, 'r') as f:
			text = f.read().replace('\n', '¤')  # punkt tokenizer handles newlines not so nice

		#Process only articles having more than 100 words
		#if len(text.split()) <= 100 :
		#	continue

		sentenced_text = sentence_analyzer.tokenize(text)
		vecr = CountVectorizer(vocabulary=wrdvecs.index)

		sentence_vectors = vecr.transform(sentenced_text).dot(wrdvecs)

		penalty = get_penalty([sentence_vectors], segment_len)
		#print('penalty %4.2f' % penalty)

		segments = []

		if penalty > 0:
			optimal_segmentation = split_optimal(sentence_vectors, penalty, seg_limit=250)
			segmented_text = get_segments(sentenced_text, optimal_segmentation)
			seg_count = 0

			for s in segmented_text:
			    #print(str(seg_count)+",")
			    segment = ""
			    for ss in s:
			        #print(re.sub('\W+',' ', ss))
			        segment += re.sub('\W+',' ', ss)
			    #print("\n")
			    segments.append(segment)    
			    seg_count += 1

			#print('%d sentences, %d segments, avg %4.2f sentences per segment' % (
			#    len(sentenced_text), len(segmented_text), len(sentenced_text) / len(segmented_text)))

			#Code For Finding External Gaps

			np.random.seed(2018)

			data_text = pd.DataFrame(segments, columns = ['text'])
			data_text['index'] = data_text.index
			documents = data_text

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

			'''
			for idx, topic in lda_model.print_topics(-1):
			    print('Topic: {} \n======\nWords: {}'.format(idx, topic))
			'''

			M = []
			count = 0
			for bow_doc in bow_corpus:
				M_r = [0]*len(documents)
				for index, score in sorted(lda_model[bow_doc], key=lambda tup: -1*tup[1]):
					M_r[index] = score
				M.append(M_r)
				count += 1

			#print("External Knowledge Gaps:-")

			no_gaps = 0
			threshold = 1.75

			for i in range(len(M)-1):
				tmp_sum = 0	
				for j in range(len(M[0])):
					tmp_sum += abs(M[i+1][j]-M[i][j])
				if tmp_sum > threshold:
					no_gaps += 1	
					#print("Gap found between segments", i+1, "and", i+2)

			f_out.write("Filename: "+str(filename)+"\n")
			f_out.write("Sentences: "+str(len(sentenced_text))+"\nSegments: "+str(len(segmented_text))+"\nKnowledge Gaps: "+str(no_gaps)+"\n")
		else:
			segments.append(text)
			f_out.write("Filename: "+str(filename)+"\n")
			f_out.write("Sentences: "+str(len(sentenced_text))+"\nSegments: 1\nKnowledge Gaps: 0\n")

		#Code for Readability Measures

		flesh_list = []
		coleman_list = []
		ari_list = []
		#print("file:", filename)

		for segment in segments:
			seg_text = segment.replace('¤', '\n')
			#print("seg len:", len(seg_text.split()))
			flesh_list.append(textstat.flesch_kincaid_grade(seg_text))
			coleman_list.append(textstat.coleman_liau_index(seg_text))
			ari_list.append(textstat.automated_readability_index(seg_text))

		f_out.write("Flesch Kincaid Grade Values: "+str(flesh_list)+"\n")
		f_out.write("Flesch Kincaid Grade CV: "+str(variation(flesh_list, axis = 0))+"\n")
		f_out.write("Coleman Liau Index Values: "+str(coleman_list)+"\n")
		f_out.write("Coleman Liau Index CV: "+str(variation(coleman_list, axis = 0))+"\n")
		f_out.write("Automated Readability Index Values: "+str(ari_list)+"\n")
		f_out.write("Automated Readability Index CV: "+str(variation(ari_list, axis = 0))+"\n")


		#Code to get edit and bytes info

		url1 = 'https://en.wikipedia.org/wiki/'
		title = filename.replace(".txt", "").replace(" ", "_")
		#For articles having view info as prefex
		if title.find("$#@") != -1:
			title = title.split("$#@")[1]
		url2 = '?action=info'

		response = requests.get(url1+title+url2)

		if response :
			soup = BeautifulSoup(response.content, 'html.parser')
			if soup.find(id='mw-pageinfo-edits') and soup.find(id='mw-pageinfo-length'):
				edits = soup.find(id='mw-pageinfo-edits').find_all("td")[1].text.replace(",", "")
				bytes_count = soup.find(id='mw-pageinfo-length').find_all("td")[1].text.replace(",", "")
				f_out.write("Edits: "+edits+"\n")
				f_out.write("Bytes: "+bytes_count+"\n")
			else:	
				f_out.write("Edits: HTML_error\n")
				f_out.write("Bytes: HTML_error\n")
		else:
			f_out.write("Edits: Network_error\n")
			f_out.write("Bytes: Network_error\n")

		f_out.write("\n")

		print(filename, "processed")

	print("Execution Time", datetime.now() - startTime)

#########################################################################################################################################

import random

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
    return np.mean(penalties)


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


######################################################################################################################################

from numpy.linalg import norm
from collections import namedtuple
Segmentation = namedtuple('Segmentation', 'total splits gains min_gain optimal')

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
