'''
Author:CherryXuan
Email:shenzexuan1994@foxmail.com
Wechat:cherry19940614

Name:利用爬虫，调用有道翻译，实现机器翻译
File:youdao_post.py
Version:v0.0.1
Date:2019/9/24 15:11
'''
import requests
import json
from aip import AipSpeech
from Shenma.sound import *




class Translation(object):
    def __init__(self, filePath, APP_ID, API_KEY, SECRET_KEY, from_ = 'AUTO', to = 'AUTO'):
        '''
        设置参数
        :param from_: 原文语种
        :param to: 译文语种
        '''
        self.from_ = from_
        self.to = to
        client = SpeechClient(APP_ID, API_KEY, SECRET_KEY)
        wav = read_wav(filePath)
        word = client.asr(wav ,'wav' , 16000 , {'dev_pid': 1537,})
        self.word = word['result'][0]
        

    def result(self):
        # _o要去掉，否则会出先error_code:50的报错
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3902.4 Safari/537.36'
        }
        data = {
            'i': self.word,
            'from': self.from_,
            'to': self.to,
            'doctype': 'json',
        }

        response = requests.post(url,data,)
        result = response.text
        result = json.loads(result)
        src = result[ 'translateResult'][0][0]['src']
        tgt = result[ 'translateResult'][0][0]['tgt']
        print('原文：{}\n译文：{}\n'.format(src, tgt))





