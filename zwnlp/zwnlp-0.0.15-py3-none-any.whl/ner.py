from pathlib import Path
from pyhanlp import HanLP, JClass
from stanza.server import CoreNLPClient

from zwnlp.utils import Backend
from zwutils.logger import logger
LOG = logger(__name__)

class NER(object):
    '''实体识别'''
    def __init__(self, cfg, backend=None):
        self.backend = backend or Backend.corenlp
        self.tags = ['nb', 'nba', 'nbp', 'nf', 'nh', 'nhd', 'nhm', 'ni', 'nic', 'nit', 'nmc',
                    'g', 'gb', 'gbc', 'gc', 'gg', 'gi', 'gm', 'gp',
                    'nr','nr1','nr2','nrf','nrj','nt','ntc','ntcb','ntcf','ntch','nth','nto','nts','ntu']
        self.corenlp_tags = ['PERSON', 'LOCATION', 'ORGANIZATION', 'COUNTRY', 'CITY', 'STATE_OR_PROVINCE']
        self.corenlp_ignore_tags = ['O','TITLE', 'DATE', 'TIME', 'MONEY', 'PERCENT']
        self.markhtml = '<mark onclick="onEntityClick(this)" data-etype="{nature}">{word}</mark>'
        self.corenlp_zh = None
        self.corenlp_en = None
        if hasattr(cfg, 'corenlp'):
            corenlp_cfg = cfg.corenlp
            classpath_default = str( Path('./corenlp').resolve() )
            classpath_default = '"%s/*"' % classpath_default
            self.corenlp_clspath = corenlp_cfg.get('homepath', classpath_default)
            self.corenlp_memsize = corenlp_cfg.get('memsize', '5G')
            self.corenlp_timeout = corenlp_cfg.get('timeout', 30000)
            self.corenlp_endpoint_zh = corenlp_cfg.get('endpoint_zh', 'http://localhost:9000')
            self.corenlp_endpoint_en = corenlp_cfg.get('endpoint_en', 'http://localhost:9000')

    def __enter__(self):
        if self.backend == Backend.corenlp:
            CoreNLPClient.CHECK_ALIVE_TIMEOUT = 480
            self.corenlp_zh = CoreNLPClient(start_server=False, annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref']
                , endpoint=self.corenlp_endpoint_zh
                , timeout=self.corenlp_timeout
                , memory=self.corenlp_memsize
                , classpath=self.corenlp_clspath)
            self.corenlp_en = CoreNLPClient(start_server=False, annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref']
                , endpoint=self.corenlp_endpoint_en
                , timeout=self.corenlp_timeout
                , memory=self.corenlp_memsize
                , classpath=self.corenlp_clspath)
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def close(self):
        if self.corenlp_zh:
            self.corenlp_zh = None
        if self.corenlp_en:
            self.corenlp_en = None

    def ner(self, sentences, lang='en'):
        rtn = []
        tags = {}
        if Backend.hanlp == self.backend:
            segment = HanLP.newSegment()\
                .enableNameRecognize(True)\
                    .enableTranslatedNameRecognize(True)\
                        .enableOrganizationRecognize(True)\
                            .enablePlaceRecognize(True)
            for sentence in sentences:
                term_list = segment.seg(sentence)
                terms = []
                for o in term_list:
                    word = o.word
                    nature = str(o.nature)
                    if nature in self.tags:
                        terms.append( (word, nature) )
                rtn.append( (sentence, terms) )
        elif Backend.corenlp == self.backend:
            corenlp = self.corenlp_en if lang == 'en' else self.corenlp_zh
            for sentence in sentences:
                ann = corenlp.annotate(sentence)
                terms = []
                for s in ann.sentence:
                    term_list = s.token
                    for o in term_list:
                        word = o.word
                        nature = o.ner
                        nature = nature.upper().strip()
                        begchar = o.beginChar
                        endchar = o.endChar
                        if nature in self.corenlp_tags:
                            if len(terms)>0 and terms[-1][1] == nature and terms[-1][3] == begchar-1:
                                _t = terms[-1]
                                terms[-1] = ('%s %s'%(_t[0], word), _t[1], _t[2], endchar)
                                continue
                            terms.append( (word, nature, begchar, endchar) )
                rtn.append( (sentence, terms) )
        
        for idx, arr in enumerate(rtn):
            # merge tags
            if Backend.corenlp == self.backend:
                cur_tag = None
                terms = arr[1]
                new_terms = []
                j = 0
                is_expend = False
                for i, term in enumerate(terms):
                    if i<j+1 and is_expend:
                        continue
                    is_expend = False
                    new_txt = [term[0]]
                    cur_tag = term[1]
                    cur_sta = term[2]
                    cur_end = term[3]
                    for j in range(i+1, len(terms)):
                        next_term = terms[j]
                        next_term_txt = next_term[0]
                        next_term_tag = next_term[1]
                        next_term_sta = next_term[2]
                        next_term_end = next_term[3]
                        if next_term_sta == cur_end and next_term_tag == cur_tag:
                            new_txt.append(next_term_txt)
                            cur_end = next_term_end
                            is_expend = True
                        else:
                            break
                    new_term = (''.join(new_txt), cur_tag, cur_sta, cur_end)
                    new_terms.append(new_term)
                rtn[idx] = (rtn[idx][0], new_terms)

        for arr in rtn:
            terms = arr[1]
            for term in terms:
                tag = term[1]
                if tag in tags:
                    if term[0] not in tags[tag]:
                        tags[tag].append(term[0])
                else:
                    tags[tag] = [term[0]]
        return rtn, tags
    
    def html(self, ners):
        rtn = []
        for a in ners:
            text = a[0] # sentence text
            terms = a[1] # terms in sentence
            text_arr = []
            last_idx = None
            for i,term in enumerate(terms):
                word = term[0]
                nature = term[1]
                # TODO 重复实体名问题
                if self.backend == Backend.corenlp:
                    bef_start = 0 if i==0 else terms[i-1][3]
                    bef_end = term[2]
                    if bef_start != bef_end:
                        text_arr.append(text[bef_start:bef_end])
                    text_arr.append(self.markhtml.format(word=word, nature=nature))
                    last_idx = bef_end + len(word)
                else:
                    text = text.replace(word, self.markhtml.format(word=word, nature=nature))
            if self.backend == Backend.corenlp:
                last = text[last_idx:] if last_idx is not None else text
                text_arr.append(last)
                text = ''.join(text_arr)
            rtn.append(text)
        rtn = ['<p>%s</p>'%s for s in rtn]
        return ''.join(rtn)
