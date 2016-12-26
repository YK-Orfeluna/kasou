# -*- coding: utf-8 -*

import pyfirmata
from config import *

board = pyfirmata.Arduino(PORT)			# Connect to Arduino

it = pyfirmata.util.Iterator(board)		# Preparation to read Analog-pin
it.start()

curve = board.get_pin('a:%s:i' %CURVE)
right = board.get_pin('a:%s:i' %RIGHT)
press = board.get_pin('a:%s:i' %PRESS)

print("Connect Arduino")

while True :
	frameRate(10)

	curve_value = curve.read()		# Read value of curve-sensro
	right_value = right.read()		# Read value of right-sensor
	press_value = press.read()		# Read value of press-sensor

	print("Sensor-Value, Curve - Right - Press : %s - %s - %s" %(curve_value, right_value, press_value)) 

	if False :
		if LEVEL1 <= curve_value < LEVEL2:
			board.digital[LED5].write(1)

		elif LEVEL2 <= curve_value < LEVEL3 :
			board.digital[LED4].write(1)
			
		elif LEVEL3 <= curve_value < LEVEL4 :
			board.digital[LED3].write(1)

		elif LEVEL4 <= curve_value < LEVEL5 :
			board.digital[LED2].write(1)

		elif LEVEL5 <= curve_value :
			board.digital[LED1].write(1)

	else :
		for i in LED :
			board.digital[i].write(0)
		exit()

