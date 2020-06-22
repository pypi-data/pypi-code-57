import requests
import pickle

url = "http://localhost:8081/worker/%s"
data = dict(uuid="abc1", greetings="hello", to="world")

r = requests.post(url % "say-hello", data=pickle.dumps(data))
r = requests.post(url % "upper-greetings", data=pickle.dumps(data))
r = requests.post(url % "dictionary", data=pickle.dumps(dict(uuid="abc2")))
