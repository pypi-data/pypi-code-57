#coding=utf-8
from uiautomator import device as d
import chardet

url = 'https://v.douyin.com/J8F1rrY/'
heads={
    "User-Agent":"okhttp/3.11.0",
    "Accept-Encoding":"gzip",
#      "Host":"v.douyin.com",
#      "Connection":"Keep-Alive"
     }
        
r = d.request.get(url, headers=heads)
print r
