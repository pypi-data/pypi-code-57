import sys
sys.path.append('./')

from advanced_led_control.led_controller import *

import advanced_led_control.models.colors as c
from advanced_led_control.models.leds import *
from advanced_led_control.models.ValueIndication import *
from advanced_led_control.models.Indicator       import *
from advanced_led_control.models.Procedure       import *

import logging

HelloWorld()

logging.basicConfig(level=logging.INFO)

def indic1_func():
	# Indication values are best shown between 1 and 10
	value_indication = ValueIndication(c.RED, 10)
	return value_indication

def indic2_func():
	value_indication = ValueIndication(c.BLUE, NO_FLICKER)
	return value_indication

indic1 = Indicator(m_col=c.GREEN, func=indic1_func, i_time=4)
indic2 = Indicator(m_col=c.GREEN, func=indic2_func, i_time=4)

stick = blinkstick.find_first()
procedure = Procedure(stick=stick, mode_led=LED_2, quiet=10, sync_duration=10)

procedure.indicators.append(indic1)
procedure.indicators.append(indic2)

procedure.run()

