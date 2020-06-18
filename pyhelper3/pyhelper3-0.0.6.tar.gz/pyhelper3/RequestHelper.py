# -*- coding: utf-8 -*-
import yaml,threading,queue,time,requests
from concurrent.futures import ThreadPoolExecutor
class RequestHelper():
    __header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    #构建一个队列
    def __init__(self,headers=None,proxy_host=None,proxy_port=None,timeout=10,thread_number=10,callback_func=None,**keyargs):
        self.header = RequestHelper.__header
        self.proxy = None
        self.callback_func = callback_func
        self.args = keyargs
        self.kwargs = None
        self.stop_flag = False
        self.thread_pool = ThreadPoolExecutor(thread_number)
        if headers:
            self.header = headers
        if proxy_host and proxy_port:
            self.proxy = {
                "http": "http://"+proxy_host+":"+str(proxy_port),
                "https": "https://"+proxy_host+":"+str(proxy_port)
            }
        self.timeout = timeout

    def get(url):
        ret = requests.get(url, headers=self.header, proxies=self.proxy, timeout=self.timeout)
        return ret
    def post(url):
        ret = requests.post(url, headers=self.header, proxies=self.proxy, timeout=self.timeout)
        return ret

    def run(self,url):
        try:
            response = requests.get(url, headers=self.header, proxies=self.proxy, timeout=self.timeout)
            # Website encode response.encoding
            # response.apparent_encoding
            response.encoding = response.apparent_encoding
            if self.callback_func:
                if self.args:
                    self.callback_func(self.args,response)
                else:
                    self.callback_func(response)
        except Exception as e:
            print(e)
    def put(self,url):
        self.thread_pool.submit(self.run,url)
    def stop(self):
        self.thread_pool.close()





