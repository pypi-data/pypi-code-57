#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'weibo_2_album'

import cached_url
import yaml
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result
from telegram_util import getWid, matchKey
import sys
import os
from PIL import Image

prefix = 'https://m.weibo.cn/statuses/show?id='

def getRetweetCap(json):
	json = json.get('retweeted_status')
	if not json:
		return ''
	return json.get('longText', {}).get('longTextContent') or json['text']

def isprintable(s):
    try: 
    	s.encode('utf-8')
    except UnicodeEncodeError: return False
    else: return True

def getPrintable(s):
	return ''.join(x for x in s if isprintable(x))

def isLongPic(path):
	ext = os.path.splitext(path)[1] or '.html'
	cache = 'tmp/' + cached_url.getFileName(path) + ext
	img = Image.open(cache)
	w, h = img.size
	return h > w * 2.1

def getHash(json):
	text = getPrintable(json['text'] + '\n\n' + getRetweetCap(json)).replace('转发微博', '')
	b = BeautifulSoup(text, features="lxml")
	return hash(b.text)

def getCap(json):
	text = getPrintable(json['text'] + '\n\n' + getRetweetCap(json)).replace('转发微博', '')
	b = BeautifulSoup(text, features="lxml")
	for elm in b.find_all('a'):
		if not elm.get('href'):
			continue
		if matchKey(elm.get('href'), ['weibo.cn/p', 'weibo.cn/search', 'weibo.com/show']):
			elm.replaceWith(elm.text)
			continue
		if '@' == elm.text[:1]:
			elm.decompose()
			continue
		md = '[%s](%s)' % (elm.text, elm['href'])
		elm.replaceWith(BeautifulSoup(md, features='lxml').find('p'))
	line = BeautifulSoup(str(b).replace('<br/>', '\n'), features='lxml').text.strip()
	line = line.replace("//:", '')
	return line

# should put to some util package, 
# but I don't want util to be dependent on cached_url
def isAnimated(path): 
	cached_url.get(path, force_cache=True, mode='b')
	gif = Image.open(cached_url.getFilePath(path))
	try:
		gif.seek(1)
	except EOFError:
		return False
	else:
		return True

def enlarge(url):
	candidate = url.replace('orj360', 'large')
	candidate_content = cached_url.get(candidate, mode='b', force_cache = True)
	if (0 < len(candidate_content) < 1 << 22 or isLongPic(candidate) or 
		isAnimated(candidate)):
		return candidate
	return url
	
def getImages(json):
	return [enlarge(x['url']) for x in json.get('pics', [])]

def getVideo(json):
	return json.get('page_info', {}).get('media_info', {}).get(
		'stream_url_hd', '')

def get(path):
	wid = getWid(path)
	r = Result()
	try:
		json = yaml.load(cached_url.get(prefix + wid), Loader=yaml.FullLoader)
	except:
		return r
	json = json['data']
	if 'test' in sys.argv:
		with open('tmp/%s.json' % wid, 'w') as f:
			f.write(str(json))
	r.imgs = getImages(json) or getImages(json.get('retweeted_status', {}))
	r.cap_html = json['text']
	r.title = json['status_title']
	r.cap = getCap(json)
	r.video = getVideo(json) or getVideo(json.get('retweeted_status', {}))
	r.wid = json.get('id')
	r.rwid = json.get('retweeted_status', {}).get('id', '')
	r.hash = getHash(json)
	r.url = path
	return r

	

