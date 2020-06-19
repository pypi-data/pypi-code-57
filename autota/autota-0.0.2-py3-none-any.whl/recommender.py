from .model import PretrainedBert
from .util import PDFProcessor
from scipy.spatial.distance import cosine
from operator import itemgetter
import numpy as np

class Recommender(object):
    def __init__(self, pdf_path, num_page, api_url, api_port):
        pdf = PDFProcessor(file_path=pdf_path)
        pages_content = []
        for page in range(pdf.pageCount):
            pages_content.append(','.join(pdf.get_page_text(page + 1)))
        self.pages_content = pages_content
        self.bert_model = PretrainedBert(api_url=api_url, api_port=api_port)
        self.pages_embedding = self.bert_model.encode(self.pages_content)
        self.num_page = num_page

    def guiding_from(self, ta_ans):
        concept = self.bert_model.encode([ta_ans])[0]
        page_distence = []
        for page_no, embedding in enumerate(self.pages_embedding):
            if np.count_nonzero(embedding) == 0:
                distance = np.inf
            else:
                distance = cosine(embedding, concept)
            page_distence.append((page_no, distance))
        page_distence = sorted(page_distence, key=itemgetter(1))
        return page_distence[:self.num_page]
