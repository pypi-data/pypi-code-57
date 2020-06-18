import requests

def convert(num):
	return ("{:,}".format(num))
class COVID:
	def __init__(self,country):
		self.country = country
	def continent(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		conti = data["continent"]
		return conti
	def total_cases(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		tootalcases = data["cases"]
		totalcases = convert(int(tootalcases))
		return totalcases
	def today_cases(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		toodaycase = data["todayCases"]
		todaycase = convert(int(toodaycase))
		return todaycase
	def total_deaths(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		deeaths = data["deaths"]
		deaths = convert(int(deeaths))
		return deaths
	def today_deaths(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		toodaydeath = data["todayDeaths"]
		todaydeath = convert(int(toodaydeath))
		return todaydeath
	def recovered(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		reecoverd = data["recovered"]
		recoverd = convert(int(reecoverd))
		return recoverd
	def active_cases(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		actiivecases = data["active"]
		activecases = convert(int(actiivecases))
		return activecases
	def tests(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		teests = data["tests"]
		test = convert(int(teests))
		return test
	def flag(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		flag = data["countryInfo"]["flag"]
		return flag
	def critical_cases(self):
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		data = qq.json()
		critcaal = data["critical"]
		critical = convert(int(critcaal))
		return critical