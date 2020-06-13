#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'twitter_2_album'

import yaml
from telegram_util import AlbumResult as Result
from telegram_util import compactText, matchKey
import tweepy
import json
import html

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
auth = tweepy.OAuthHandler(CREDENTIALS['twitter_consumer_key'], CREDENTIALS['twitter_consumer_secret'])
auth.set_access_token(CREDENTIALS['twitter_access_token'], CREDENTIALS['twitter_access_secret'])
twitterApi = tweepy.API(auth)

def getTid(path):
	index = path.find('?')
	if index > -1:
		path = path[:index]
	return path.split('/')[-1]

def getCap(status):
	text = list(status.full_text)
	for x in status.entities.get('media', []):
		for pos in range(x['indices'][0], x['indices'][1]):
			text[pos] = ''
	text = html.unescape(''.join(text))
	text = compactText(text)
	return text

def getEntities(status):
	try:
		return status.extended_entities
	except:
		return status.entities

def getImgs(status):
	if not status:
		return []
	# seems video is not returned in side the json, there is nothing we can do...
	return [x['media_url'] for x in getEntities(status).get('media', [])
		if x['type'] == 'photo']

def getVideo(status):
	if not status:
		return ''
	videos = [x for x in getEntities(status).get('media', []) if x['type'] == 'video']
	if not videos:
		return ''
	variants = [x for x in videos[0]['video_info']['variants'] if x['content_type'] == 'video/mp4']
	variants = [(x.get('bitrate'), x) for x in variants]
	variants.sort()
	return variants[-1][1]['url']

def getQuote(status, func):
	try:
		status.quoted_status
	except:
		return None
	return func(status.quoted_status)

def get(path):
	tid = getTid(path)
	status = twitterApi.get_status(tid, tweet_mode="extended")
	r = Result()
	r.video = getVideo(status) or getQuote(status, getVideo) or ''
	r.imgs = getImgs(status) or getQuote(status, getImgs) or []
	r.cap = getCap(status)
	if matchKey(path, ['twitter', 'http']):
		r.url = path
	else:
		r.url = 'http://twitter.com/%s/status/%s' % (
			status.user.screen_name or status.user.id, tid)
	return r
