from .model import TextRank, PretrainedBert
from .util import PDFProcessor
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sklearn.metrics.pairwise import cosine_similarity
from bert_serving.client import BertClient
from difflib import SequenceMatcher 
import jieba

class Grader(object):
    def __init__(self, pdf_path, bert_api_url, bert_api_port, n_word=5, word_min_len=2, sentence_min_len=6):
        self.pdf = PDFProcessor(pdf_path)
        self.text = self.pdf.get_pdf_text()

        self.summarize_model = TextRank(n_word=n_word, word_min_len=word_min_len, sentence_min_len=sentence_min_len)
        self.bert_model = PretrainedBert(api_url=bert_api_url, api_port=bert_api_port)
        self.slides_embedding = self.bert_model.encode([self.text])
        
        self.keywords = self.summarize_model.get_keywords(self.text)
        self.key_sentences = self.summarize_model.get_key_sentences(self.keywords, self.text)
    
    def grade_marker(self, marker_text):
        chencherry = SmoothingFunction()
        reference = self.key_sentences
        candidate = marker_text
        bleu = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=chencherry.method1)
        return bleu

    def grade_memo(self, memo_text):
        #get length
        length = len(memo_text) 

        #get longest common sequence
        seqMatch = SequenceMatcher(None, self.text, memo_text)
        match = seqMatch.find_longest_match(0, len(self.text), 0, len(memo_text))
        lcs = match.size 

        #get semantic similarity
        memo_embedding = self.bert_model.encode([memo_text])
        semantic_similarity = cosine_similarity(memo_embedding, self.slides_embedding)
        if semantic_similarity <= 0:
            semantic_similarity = 0.1
        else:
            semantic_similarity = semantic_similarity[0][0]

        #get keyword hit ratio
        tokens = jieba.cut(memo_text)
        hit_kw = list(set(tokens).intersection(set(self.keywords)))
        kw_hit_ratio = 0.8 + len(hit_kw) / len(self.keywords)

        memo_score = (length - lcs)*semantic_similarity*kw_hit_ratio
        return memo_score


# class ShortAnswerGrader(object):