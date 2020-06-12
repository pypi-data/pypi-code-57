import sys
sys.path.append('./')

from advanced_led_control.models.leds import *
from advanced_led_control.models.ValueIndication import *
from advanced_led_control.models.Indicator       import *
from advanced_led_control.models.Procedure       import *

import logging

import psutil

logging.basicConfig(level=logging.ERROR)

def get_val_ind(num):

	val = ValueIndication('blue', NO_FLICKER)

	if num <= 40:
		val.col = 'green'
	elif num <= 60:
		val.col = 'yellow'
	elif num <= 80:
		val.col = 'orange'
		val.flicker = 1
	elif num > 80:
		val.col = 'red'
		val.flicker = num - 80

	return val

def indic1_func():
	cpu = psutil.cpu_percent()

	val = get_val_ind(cpu)
	print("cpu: " + str(cpu) +" (" + val.col + ": " + str(val.flicker) + ")")

	return val

def indic2_func():
	virt_mem = psutil.virtual_memory()
	mem = virt_mem.percent

	val = get_val_ind(mem)
	print("mem: " + str(mem) +" (" + val.col + ": " + str(val.flicker) + ")")

	return val

def indic3_func():
	du = psutil.disk_usage('/').percent

	val = get_val_ind(du)
	print("du: " + str(du) +" (" + val.col + ": " + str(val.flicker) + ")")

	return val

def indic4_func():
	f = open("/sys/class/thermal/thermal_zone0/temp", "r")
	temp_text = f.read()
	f.close()
	temp = int(temp_text) / 1000.0

	val = get_val_ind(temp)
	print("temperature: " + str(temp) +" (" + val.col + ": " + str(val.flicker) + ")")

	return val

indic1 = Indicator(m_col='aqua', func=indic1_func, brightness = 0.1, i_time=4)
indic2 = Indicator(m_col='orchid', func=indic2_func, brightness = 0.1, i_time=4)
indic3 = Indicator(m_col='whitesmoke', func=indic3_func, brightness = 0.1, i_time=4)
indic4 = Indicator(m_col='mistyrose', func=indic4_func, brightness = 0.1, i_time=4)

stick = blinkstick.find_first()
procedure = Procedure(stick=stick, mode_led=LED_2, quiet=10, sync_duration=20)

procedure.indicators.append(indic1)
procedure.indicators.append(indic2)
procedure.indicators.append(indic3)
procedure.indicators.append(indic4)

procedure.run()

