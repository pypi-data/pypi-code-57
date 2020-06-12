from .colors import *
from .modes import *
from .color_types import *

import time
import logging

from blinkstick import blinkstick

NO_FLICKER = 1001
FLICKER_MAX = 1000
MIN_FLICKER_DURATION = 30 # ms, consists of both on and off time
													# 24 fps is the maximum we can easily notice
													# 1000ms/24fps ~= 40ms, we picked 30 to be even more

class Indicator:
	""" Indicator class. """
	def __init__(self, m_col=GREEN, speed=1, brightness=1, func=None, i_time=4):
		self.m_col      = m_col # mode color
		self.speed      = speed
		self.brightness = min(max(brightness,0), 1) # valid range [0, 1]
		self.func       = func
		self.i_time     = i_time # indication time in seconds

	def indicate(self, stick, mode_led, active_time):
		col = self.m_col
		val_led = 1-mode_led

		col_type = get_col_type(col)
		set_color(stick=stick, index=mode_led, col=col, col_type=col_type)

		# Run the callback
		value_indication = self.func()
		col = value_indication.col
		flicker = value_indication.flicker

		logging.debug("Indication Callback returned color: %s, flicker: %d",
									col, flicker)

		flicker_time = float(FLICKER_MAX)/flicker # in ms as FLICKER_MAX is 1000
		flicker_time = max(flicker_time, MIN_FLICKER_DURATION) # set minimum

		# Use if we want to even flicker as long as we didn't reach the maximum
		# Most probably will get the led earlier to EOL B-)
		if (flicker >= NO_FLICKER):
		# Use if we want to stop flickering as long before even reaching the maximum
		# but rather based on the MIN_FLICKER_DURATION
		#if (flicker > FLICKER_MAX or flicker_time == MIN_FLICKER_DURATION):
			logging.info("Fixed for %1.2fs", active_time)
			col = get_rgb(col) # enforce using rgb
			col_type = get_col_type(col)
			col = get_brightness_mod(col, self.brightness)
			set_color(stick=stick, index=val_led, col=col, col_type=col_type)
			time.sleep(active_time)

		else:
			one_flicker  = flicker_time / 2	# a pulse is defined by the delay of either on or off

			active_time_ms = active_time*1000
			logging.info("Flickering for %1.2fs", active_time)
			repeats = active_time_ms/flicker_time

			repeats = max(repeats, 1) # minimum is one repeat

			# TODO:start pulsing in a different thread and stop it when exact active_time is over
			logging.debug("Flickering for %d times, with duration %dms each on and each off",
										repeats, one_flicker)
			col = get_rgb(col) # enforce using rgb
			col_type = get_col_type(col)
			col = get_brightness_mod(col, self.brightness)
			set_pulse(stick=stick, index= val_led, col=col, col_type=col_type,
								repeats=int(repeats), duration=int(one_flicker), steps=10)

def get_brightness_mod(col, brightness):
	rgb_col = get_rgb(col)
	#return map(lambda x: x * float(brightness), rgb_col)
	return [x * float(brightness) for x in rgb_col]

def get_rgb(col):
	"""Change to RGB if needed
	@param col: either hexadecimal or RGB
	@return: RGB format
	"""
	col_type = get_col_type(col)

	if col_type == CT_HEX:
		return hex_to_rgb(col)

	elif col_type == CT_NAME:
		stick = blinkstick.BlinkStick()
		h = stick._names_to_hex[col]
		return hex_to_rgb(h)

	elif col_type == CT_RGB:
		return col

def hex_to_rgb(hex_col):
	h = hex_col.lstrip('#')
	return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_col_type(col):
	if isinstance(col, str):
		if col.startswith('#'):
			return CT_HEX
		else:
			return CT_NAME
	elif len(col) == 3:
		return CT_RGB
	else:
		# panic
		logging.error("Unsupported color type!")
		return CT_DEFAULT

def set_color(stick, index, col, col_type):
	""" Set blinkstick color
	Only RGB is used to be able to further control the brightness
	
	Arguments:
			stick {BlinkStick} -- [description]
			index {int} -- led to set
			col {list|string} -- either list of RGB or hex string or CSS name string 
			col_type {int} -- either CT_RGB, CT_HEX or CT_NAME
	"""
	if (col_type == CT_RGB):
		curr_col = stick.get_color(index=index, color_format='rgb')
		if curr_col != col:
			stick.set_color(index=index, red=col[0], green=col[1], blue=col[2])
	elif (col_type == CT_NAME): # deprecated
		# comparison takes place in the hex domain
		curr_col = stick.get_color(index=index, color_format='hex')
		col = stick._names_to_hex[col]
		if curr_col != col:
			stick.set_color(index=index, hex=col)
	elif (col_type == CT_HEX): # deprecated
		curr_col = stick.get_color(index=index, color_format='hex')
		if curr_col != col:
			stick.set_color(index=index, hex=col)

def set_pulse(stick, index, col, col_type, repeats, duration, steps):
	""" Pulse the blinkstick
	CSS names are problematic here, Don't work!
	so we either convert to HEX or RGB, we decided to use RGB for further control
	of brightness

	Arguments:
			stick {BlinkStick} -- [description]
			index {int} -- led to set
			col {list|string} -- either list of RGB or hex string or CSS name string 
			col_type {int} -- either CT_RGB, CT_HEX or CT_NAME
			repeats {int} -- number of pulses
			duration {int} -- on/off time in ms 
			steps {int} -- gradiant steps for each pulse
	"""
	if (col_type == CT_RGB):
		stick.pulse(index=index, red=col[0], green=col[1], blue=col[2],
								repeats=repeats, duration=duration, steps=steps)
	elif (col_type == CT_NAME): # deprecated
		stick.pulse(index=index, name=col,
								repeats=repeats, duration=duration, steps=steps)
	elif (col_type == CT_HEX): # deprecated
		stick.pulse(index=index, hex=col,
								repeats=repeats, duration=duration, steps=steps)
