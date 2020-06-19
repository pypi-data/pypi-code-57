import requests
import json

class GET:
	def getDog(self):
		response = requests.get('https://some-random-api.ml/img/dog')
		json_data = json.loads(response.text)

		return json_data['link']

	def getCat(self):
		response = requests.get('https://some-random-api.ml/img/cat')
		json_data = json.loads(response.text)

		return json_data['link']

	def getFox(self):
		response = requests.get('https://some-random-api.ml/img/fox')
		json_data = json.loads(response.text)

		return json_data['link']

	def getMeme(self):
		response = requests.get('https://some-random-api.ml/meme')
		json_data = json.loads(response.text)

		return json_data['image']