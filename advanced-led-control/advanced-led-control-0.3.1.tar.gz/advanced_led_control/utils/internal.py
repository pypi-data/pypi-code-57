from blinkstick import blinkstick
import time
import sys, signal

import logging

# Initialization wait per second
INIT_SLEEP = 0.05

NUM_OF_LEDS = 2

# Follow https://www.blinkstick.com/help/tutorials/blinkstick-pro-modes
NORMAL_MODE  = 0
INVERSE_MODE = 1
WS2812_MODE  = 2

def init_stick():
	nano = blinkstick.find_first()
	# TODO: handle if stick wasn't recognized
	nano.set_mode(WS2812_MODE)
	time.sleep(INIT_SLEEP)

def get_first_stick():
	pass

def register_graceful_shutdown(stick):
	# signal handler instance method
	shim = StickSignalHandler(stick)
	signal.signal(signal.SIGINT, shim.signal_handler)

def turn_off_stick(stick):
	logging.debug("Stopping stick %s", stick.get_serial())
	stick.turn_off()

	# turn_off doesn't automatically recognize all the leds
	# follow https://forums.blinkstick.com/t/python-only-first-led-turns-off-turn-off/452/2
	led_zeros = [0] * 3 * NUM_OF_LEDS
	stick.set_led_data(0, led_zeros)

class StickSignalHandler(object):
	def __init__(self, stick):
		self.stick = stick

	def signal_handler(self, signal, frame):
		logging.debug("Stopping based on external interrupt.")
		turn_off_stick(self.stick)
		sys.exit(0)

