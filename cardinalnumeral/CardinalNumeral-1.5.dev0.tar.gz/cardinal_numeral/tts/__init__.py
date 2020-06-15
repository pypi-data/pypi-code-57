
import time, pygame
import os
from tinytag import TinyTag
from io import BytesIO
import json
import requests
"""
pygame.mixer.init()
pygame.mixer.music.load('1.mp3')
pygame.mixer.music.play()
pygame.mixer.music.queue('2.mp3')
"""

"""
	Unknown Unicode Path Problem ?
	To avoid FileNotFoundError, FileName will have preceding base64 value

"""

import unicodedata

# TTS Module
def speak(string, address, usingCloud = True, language='vietnamese'):
	if not usingCloud:
		print(string)
		string = string.replace('-', ' ').replace(', ', ' ').replace('  ', ' ')
		strings = string.split(' ')
		# address = address.encode('utf8')
		# listFile = os.listdir(address)
		listFile = [unicodedata.normalize('NFC', f) for f in os.listdir(address)]

		# if any([not s + '.ogg' in listFile for s in string]):
		# 	raise FileNotFoundError(string, listFile, address)

		for s in strings:
			s = s.strip()
			if len(s) == 0:
				continue
			filename = (s  + '.ogg')
			if not (filename in listFile):
				raise FileNotFoundError(filename, address, listFile)

		pygame.mixer.init()
		first = True
		for word in strings:
			# TODO
			if len(word)==0:
				continue
			filepath = os.path.join(address, word + '.ogg')
			print(filepath)

			pygame.mixer.Sound(filepath).play()
			# time.sleep(0.4)
			tag = TinyTag.get(filepath)
			time.sleep(tag.duration)

	else:
		# Why stop their, its 4.0 already :D
		if language == 'vietnamese':
			url = 'https://api.fpt.ai/hmi/tts/v5'
			res = requests.post(url, params={
				'api_key': 'qhSfMYEDBwIPG3nGtTP6s31Z75zaRKsz',
				'voice': 'banmai',
				# 'speed': '+3'
			}, data = string.encode('utf8'))
			response = json.loads(res.content)
			while True:
				audio = requests.get(response['async'])
				if audio.status_code == 200:
					print('Received')
					break
		elif language == 'english' :
			url = "http://api.voicerss.org"#?key=<API key>&hl=en-us&src=Hello, world!"
			audio = requests.get(url, params={
				'key': '2a939cf49b6a4580b890d936549601e2',
				'src': string,
				'hl': 'en-us',
				'c': 'mp3',
				'f': '44khz_16bit_stereo'

			})
		with open('__temp__.mp3', 'wb') as f:
			f.write(audio.content)
		path = os.path.abspath('__temp__.mp3')
		pygame.mixer.init(44100)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			time.sleep(1)