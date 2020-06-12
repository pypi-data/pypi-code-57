import time
import datetime
import math
import logging

def start_at_sync_time(sync_seconds=10):
	t = datetime.datetime.today()

	future = get_next_run_time(t, sync_seconds)
	logging.info("Next sync run at %s", future)

	# rem_minutes = (future-t).minutes # use when minutes are supported
	rem_seconds = (future-t).seconds
	rem_milliseconds = (future-t).microseconds / 1000000.0

	# Enable only for debugging
	if False:
		print("future is ", future)
		print("t is ", t)
		print(rem_seconds + rem_milliseconds)

	time.sleep(rem_seconds + rem_milliseconds)

def get_next_run_time(t, sync_seconds=10):
	"""
	@type t: datetime
	@param t: current time
	@type t: int
	@param sync_seconds: period in seconds to sync upon
	@param sync_minutes: TODO implement
	@return: the next run time based on @sync_seconds
	"""
	newsecond = roundup(t.second, sync_seconds)

	future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,rounddown(t.second, sync_seconds))

	if newsecond >= 60:
		future = jump_minute(future)
	else:
		future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,newsecond)
		if (future < t):
			newsecond = newsecond + sync_seconds
			if newsecond >= 60:
				future = jump_minute(future)
			else:
				future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,newsecond)

	return future

def jump_minute(t):
	t += datetime.timedelta(minutes=1)
	return datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,0)

def roundup(x, nearest):
	return int(math.ceil(x / float(nearest))) * nearest

def rounddown(x, nearest):
	return int(math.floor(x / float(nearest))) * nearest

