import fitz
import os
import numpy as np
from ckippy import parse_tree
import requests


class PDFProcessor:
    def __init__(self, file_path):
        self.path = file_path
        self.doc = fitz.open(self.path)
        self.pageCount = self.doc.pageCount
        # self.text = ''
    def is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False
        
    def is_number(self, uchar):
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
        else:
            return False
        
    def is_alphabet(self, uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False
    def is_char(self, uchar):
        if not (self.is_chinese(uchar) or self.is_number(uchar) or self.is_alphabet(uchar)):
            return True
        else:
            return False
    def get_pdf_text(self):
        page_content = []
        all_page = []

        for page in self.doc:
            page_content.append(page.getText('text'))
        for page_num in range(len(page_content)):
            for j in page_content[page_num]:
                if self.is_char(j):
                    page_content[page_num] = page_content[page_num].replace(j, ',')
        for page_num in range(len(page_content)):
            page_content[page_num] = list(filter(lambda x: len(x) > 1, page_content[page_num].split(',')))

        for page in page_content:
            all_page.append(','.join(page))    
        text = '。'.join(all_page)
        return text

    def get_page_text(self, page):
        page_content = []
        # all_page = []

        for p in self.doc:
            page_content.append(p.getText('text'))
        for page_num in range(len(page_content)):
            for j in page_content[page_num]:
                if self.is_char(j):
                    page_content[page_num] = page_content[page_num].replace(j, ',')
        for page_num in range(len(page_content)):
            page_content[page_num] = list(filter(lambda x: len(x) > 1, page_content[page_num].split(',')))
        
        return page_content[page-1]
    
    def highlight(self, important_sentence):
        # doc = fitz.open(self.path)
        slide_name = self.path.split('/')[-1].replace('.pdf', '')
        for page in self.doc:
            for key_sentence, weight in important_sentence.items():
                quads = page.searchFor(key_sentence, hit_max=100, quads=True)
                page.addHighlightAnnot(quads)
        file_name = slide_name + 'marked' + '.pdf'
        store_path = os.path.join('./output_pdf', file_name)
        self.doc.save(store_path)

class SentencePreprocessor:
    def __init__(self):
        self.api_url = 'http://140.115.53.158:9453/translate'

    def is_sentence(self, text):
        tree = parse_tree(text)
        result = tree[0]
        if 'S' in result.split('(')[0] and len(text) >= 10:
            return True
        else:
            return False

    def translateToChinese(self, src_text):
        params = {'text': src_text, 'src': 'en', 'tgt': 'zh-TW'}
        resp = requests.get(self.api_url, params=params)
        return dict(resp.json())['translatedText']

    def translateToEnglish(self, src_text):
        params = {'text': src_text, 'src': 'zh-TW', 'tgt': 'en'}
        resp = requests.get(self.api_url, params=params)
        return dict(resp.json())['translatedText']

