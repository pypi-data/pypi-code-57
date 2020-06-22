import datetime as dt

# Error classes
class NotValidObject(Exception):
	"""Error raises when passed object is invalid."""
	pass

class InvalidComparison(Exception):
	"""Error raises when given time given as past is actually future or current time"""
	pass

class Formatter:
	def __init__(self):
		pass

	def get_delta(self,delta, as_dict=False):
		"""
		Convert a timedelta object to string.

		Parameters
		- delta		A time delta object
		- as_dict	Whether it should return a dictionary or a string. Default False

		return		String or dictionary according to as_dict kwarg
		"""

		if not isinstance(delta, dt.timedelta):
			raise NotValidObject(f"delta must be a object of 'datetime.timedelta' given '{type(delta).__name__}'")

		dur = ""
		days = abs(delta.days)
		seconds = abs(delta.seconds)

		year = 0
		month = 0
		day = 0
		hour = 0
		minute = 0
		second = 0

		if days == 0 and seconds == 0:
			if as_dict:
				return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
			dur = "Just now"
			return dur

		if days >= 365:
			year = days//365
			days = days%365


		if days >=30:
			month = days//30

			if month >= 12:
				year += month // 12

				month = month % 12

			days = days %30

		if days >= 0:
			day = days

		if seconds >= 3600:
			hour = seconds//3600
			seconds = seconds%3600

		if seconds >= 60:
			minute = seconds//60

			seconds = seconds%60

		if seconds > 0:
			second = seconds

		if as_dict:
			return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
		dur = f"{f'{year} Years ' if year > 0 else ''}{f'{month} Months ' if month > 0 else ''}{f'{day} Days ' if day > 0 else ''}{f'{hour} Hours ' if hour > 0 else ''}{f'{minute} Minutes ' if minute > 0 else ''}{f'{second} Seconds' if second > 0 else ''}"

		dur_list = [item for item in dur.split(" ") if not item == ""]

		if len(dur_list) > 2:

			first_part = dur_list[:len(dur_list)-2]
			last_part = [item for item in dur_list if item not in first_part]

			part1 = " ".join(first_part)
			part2 = " ".join(last_part)

			final_output = part1 + " and " + part2

			return final_output
		else:
			return dur

	def past_to_now(self,past, now, as_dict=False):
		"""Past date difference compared to current time

		Parameters
		- now		A datetime.date or datetime.datetime object represents current time
		- past		A datetime.date or datetime.datetime object represents a past date. Giving future date will raise an error.
		- as_dict	Whether it should return a dictionary or a string. Default False

		return		String or dictionary according to as_dict kwarg
		"""
		valids = [dt.date, dt.datetime]

		if type(now) not in valids or type(past) not in valids:
			raise InvalidComparison("now and past should be either object of 'datetime.date', or 'datetime.datetime'")

		if isinstance(now, dt.date):
			now = dt.datetime.combine(now, dt.datetime.min.time())

		if isinstance(past, dt.date):
			past = dt.datetime.combine(past, dt.datetime.min.time())

		dur = ""

		delta = now - past

		days = abs(delta.days)
		seconds = abs(delta.seconds)

		year = 0
		month = 0
		day = 0
		hour = 0
		minute = 0
		second = 0

		if now == past:
			if as_dict:
				return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}
			dur = "Just now"
			return dur

		if now < past:
			raise InvalidComparison("past cant be greater then now")

		if days >= 365:
			year = days//365
			days = days%365


		if days >=30:
			month = days//30

			if month >= 12:
				year += month // 12

				month = month % 12

			days = days %30

		if days >= 0:
			day = days

		if seconds >= 3600:
			hour = seconds//3600
			seconds = seconds%3600

		if seconds >= 60:
			minute = seconds//60

			seconds = seconds%60

		if seconds > 0:
			second = seconds

		if as_dict:
			return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}

		dur = f"{f'{year} Years ' if year > 0 else ''}{f'{month} Months ' if month > 0 else ''}{f'{day} Days ' if day > 0 else ''}{f'{hour} Hours ' if hour > 0 else ''}{f'{minute} Minutes ' if minute > 0 else ''}{f'{second} Seconds' if second > 0 else ''}"

		dur_list = [item for item in dur.split(" ") if not item == ""]

		if len(dur_list) > 2:

			first_part = dur_list[:len(dur_list)-2]
			last_part = [item for item in dur_list if item not in first_part]

			part1 = " ".join(first_part)
			part2 = " ".join(last_part)

			final_output = part1 + " and " + part2

			return final_output
		else:
			return dur

	def get_difference(self, datetime1, datetime2, as_dict=False):
		"""Past date difference compared to current time

		Parameters
		- datetime1	A datetime.date or datetime.datetime object
		- datetime2	A datetime.date or datetime.datetime object
		- as_dict	 	Whether it should return a dictionary or a string. Default False

		return		String or dictionary according to as_dict kwarg
		"""
		valids = [dt.date, dt.datetime]

		if type(datetime1) not in valids or type(datetime2) not in valids:
			raise InvalidComparison("datetime1 and datetime2 should be either object of 'datetime.date', or 'datetime.datetime'")

		if isinstance(datetime1, dt.date):
			datetime1 = dt.datetime.combine(datetime1, dt.datetime.min.time())

		if isinstance(datetime2, dt.date):
			datetime2 = dt.datetime.combine(datetime2, dt.datetime.min.time())

		if datetime1 < datetime2:
			datetime1, datetime2 = datetime2, datetime1

		data = self.past_to_now(datetime1, datetime2, as_dict)
		return data

	def natural_date(self, date, as_dict=False):
		"""
		datetime object to a human readable time

		Parameters
		- date				a datetime.date object
		- as_dict			Whether it should return a dictionary or a string. Default False

		return				string or dictionary according to as_dict kwarg
		"""
		if not isinstance(date, dt.date):
			raise NotValidObject("date must be a object of 'datetime.date'")

		date = dt.datetime.strftime(date, "%d")

		day_short = dt.datetime.strftime(date, "%a")
		day_full = dt.datetime.strftime(date, "%A")

		month_short = dt.datetime.strftime(date, "%b")
		month_full = dt.datetime.strftime(date, "%B")

		year_short = dt.datetime.strftime(date, "%y")
		year_full = dt.datetime.strftime(date, "%Y")

		if as_dict:
			return {'date': date, 'day_short': day_short, 'day_full': day_full, 'year_short': year_short, 'year_full': year_full, 'month_short': month_short, 'month_full': month_full, 'date': date}


		date_part = dt.datetime.strftime(date, "%A, %d %b %Y")

		return date_part

	def natural_time(self, time, as_dict=False, format=12):
		"""
		datetime object to a human readable time

		Parameters
		- time				a datetime.time object
		- as_dict			Whether it should return a dictionary or a string. Default False

		return				string or dictionary according to as_dict kwarg
		"""
		valids = [12, 24]

		if format not in valids:
			raise ValueError("for must be either 12 or 24")

		if not isinstance(time, dt.time):
			raise NotValidObject("time must be a object of 'datetime.time'")

		hour = time.hour
		minute = time.minute
		locale = None

		if format == 12:
			if hour >12:
				hour = hour-12
				locale = "PM"
			else:
				hour = hour
				locale = "AM"

			data = f"{hour}:{minute} {locale}"

		if format == 24:
			data = f"{hour}:{minute}"

		if as_dict and format == 12:
			return {'hour':hour, 'minute': minute, 'locale':locale}

		if as_dict and format == 24:
			return {'hour':hour, 'minute': minute}

		return data

	def natural_datetime(self, date_time, as_dict=False):
		"""
		datetime object to a human readable time

		Parameters
		- date_time		a datetime.datetime object
		- as_dict			Whether it should return a dictionary or a string. Default False

		return				string or dictionary according to as_dict kwarg
		"""
		if isinstance(date_time, dt.date):
			return self.natural_date(date_time, as_dict)

		if isinstance(date_time, dt.time):
			return self.natural_time(date_time, as_dict)

		date = dt.datetime.strftime(date_time, "%d")

		day_short = dt.datetime.strftime(date_time, "%a")
		day_full = dt.datetime.strftime(date_time, "%A")

		month_short = dt.datetime.strftime(date_time, "%b")
		month_full = dt.datetime.strftime(date_time, "%B")

		year_short = dt.datetime.strftime(date_time, "%y")
		year_full = dt.datetime.strftime(date_time, "%Y")

		hour = dt.datetime.strftime(date_time, "%I")
		minute = dt.datetime.strftime(date_time, "%m")
		locale = dt.datetime.strftime(date_time, "%p")

		if as_dict:
			return {'date': date, 'day_short': day_short, 'day_full': day_full, 'year_short': year_short, 'year_full': year_full, 'month_short': month_short, 'month_full': month_full, 'date': date, 'hour':hour, 'minute': minute, 'locale': locale}

		date_part = dt.datetime.strftime(date_time, "%A, %d %b %Y")
		time_part = dt.datetime.strftime(date_time, "%I:%M %p")

		return date_part + " at " + time_part

	def seconds_to_string(self, seconds, as_dict=False):
		"""Convert seconds to time"""

		seconds = int(seconds)

		year = 0
		month = 0
		day = 0
		hour = 0
		minute = 0
		second = 0

		if seconds >= 31104000:
			year = seconds // 31104000
			seconds = seconds % 31104000

		if seconds >= 2592000:
			month = seconds // 31104000
			seconds = seconds % 31104000

		if seconds >= 86400:
			days = seconds // 86400
			seconds = seconds % 86400

		if seconds >= 3600:
			hours = seconds // 3600
			seconds = seconds % 3600

		if seconds >= 60:
			minutes = seconds // 60
			seconds = seconds % 60

		if as_dict:
			return {'years': year, 'months': month, 'days' : day, 'hours': hour, 'minutes': minute, 'seconds': second}

		dur = f"{f'{year} Years ' if year > 0 else ''}{f'{month} Months ' if month > 0 else ''}{f'{day} Days ' if day > 0 else ''}{f'{hour} Hours ' if hour > 0 else ''}{f'{minute} Minutes ' if minute > 0 else ''}{f'{second} Seconds' if second > 0 else ''}"
		return dur

	def mili_to_string(self, milisecond, as_dict = False):
		seconds = int(milisecond /1000)

		return self.seconds_to_string(seconds, as_dict)
