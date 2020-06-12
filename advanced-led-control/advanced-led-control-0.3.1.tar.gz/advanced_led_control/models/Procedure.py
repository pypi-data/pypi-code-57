from .leds import *
from ..utils.internal import *
from ..utils.sync_run import *
from ..utils.GracefulKiller import GracefulKiller

import logging

class Procedure:
	""" Procedure class. """

	def __init__(self, name=None, stick=None, mode_led=LED_1, periodicity=2,
							 quiet=20, indicators=[], sync_duration=0):
		self.name = name

		self.stick       = stick
		self.mode_led    = mode_led
		self.periodicity = periodicity # deprecated
		self.quiet       = quiet

		self.indicators  = indicators

		self.sync_duration = sync_duration

	def run(self):
		init_stick()

		killer = GracefulKiller()
	
		register_graceful_shutdown(self.stick)

		while True:
			try:
				logging.debug("Start procedure loop")

				if (self.sync_duration > 0):
					start_at_sync_time(self.sync_duration)

				for indicator in self.indicators:
					activeness = self.get_active_time(indicator.i_time)
					logging.debug("Indicating active for %fs", activeness)
					indicator.indicate(self.stick, self.mode_led, activeness)

					quietness = self.get_quiet_time(indicator.i_time)
					logging.debug("Sleeping for %fs", quietness)
					turn_off_stick(self.stick)
					time.sleep(quietness)

					# turn_off doesn't automatically recognize all the leds
					if killer.kill_now:
						# Only stop between indicator runs
						break

			except Exception as e:
				turn_off_stick(self.stick)

				print >> sys.stderr, "Exiting for exception."
				print >> sys.stderr, "Exception: %s" % str(e)
				sys.exit(1)

			if killer.kill_now:
				# End the loop if the signal is received
				break


		turn_off_stick(self.stick)


	def get_quiet_time(self, indication):
		return indication * self.quiet / 100.0

	def get_active_time(self, indication):
		return indication - (indication * self.quiet / 100.0)
