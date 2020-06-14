import os
import uuid
import requests
from QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QASetting.QALocalize import cache_path
from QUANTAXIS.QAUtil.QAParameter import RUNNING_STATUS
from QUANTAXIS.QAUtil.QASetting import DATABASE


class FinancialReport(QABaseHandler):
    def get(self):
    #     self.write(requests.get('http://choicewzp1.eastmoney.com/Report/Search.do').text)
    # def post(self):

        title =  self.get_argument('title')
        limit = self.get_argument('limit')
        startDate = self.get_argument('startDate')
        endDate = self.get_argument('endDate')

        sort = self.get_argument('sort','datetime')
        order = self.get_argument('order', 'desc')
        self.write(requests.post('http://choicewzp1.eastmoney.com/Report/Search.do', data={
            'title': title, 'limit': limit, 'startDate': startDate, 'endDate': endDate, 'sort': sort, 'order': order
        }).text)