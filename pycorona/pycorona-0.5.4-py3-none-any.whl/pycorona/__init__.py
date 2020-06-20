import requests

url = None
qq = None
data = None
def convert(num):
		return (f"{num:,}")
class Country:
	def __init__(self, country):
		self.country = country
		url = f"https://disease.sh/v2/countries/{self.country}"
		qq = requests.get(url)
		global data
		data = qq.json()
	def total_cases(self):
		global data
		cases = convert(int(data["cases"]))
		return cases
	def today_cases(self):
		global data
		todaycases = convert(int(data["todayCases"]))
		return todaycases
	def continent(self):
		global data
		continent = data["continent"]
		return continent
	def total_deaths(self):
		global data
		deaths = convert(int(data["deaths"]))
		return deaths
	def today_deaths(self):
		global data
		deaths = convert(int(data["todayDeaths"]))
		return deaths
	def recovered(self):
		global data
		recovered = convert(data["recovered"])
		return recovered
	def active_cases(self):
		global data
		activecases = convert(int(data["active"]))
		return activecases
	def tests(self):
		global data
		tests = convert(int(data["tests"]))
		return tests
	def flag(self):
		global data
		flag = data["countryInfo"]["flag"]
		return flag
	def critical_cases(self):
		global data
		critical = convert(int(data["critical"]))
		return critical
class World:
	def __init__(self):
		global url
		url = f"https://disease.sh/v2/all"
		global qq
		qq = requests.get(url)
		global data
		data = qq.json()
	def affected_countries(self):
		global data
		affected = data["affectedCountries"]
		return affected
	def total_cases(self):
		global data
		cases = convert(int(data["cases"]))
		return cases
	def today_cases(self):
		global data
		cases = convert(int(data["todayCases"]))
		return cases
	def total_deaths(self):
		global data
		deaths = convert(int(data["deaths"]))
		return deaths
	def today_deaths(self):
		global data
		deaths = convert(int(data["todayDeaths"]))
		return deaths
	def recovered(self):
		global data
		recovered = convert(int(data["recovered"]))
		return recovered
	def active_cases(self):
		global data
		activecases = convert(int(data["active"]))
		return activecases
	def tests(self):
		global data
		tests = convert(int(data["tests"]))
		return tests
	def critical_cases(self):
		global data
		critical = convert(int(data["critical"]))
		return critical