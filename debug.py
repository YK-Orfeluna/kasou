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

	if True :
		if curve_value < LEVEL1 :
			for i in LED :
				board.digital[i].write(1)

		elif LEVEL1 <= curve_value < LEVEL2:
			l = [0, 1, 1, 1, 1]
			for x, i in enumerate(LED) :
				board.digital[i].write(l[x])

		elif LEVEL2 <= curve_value < LEVEL3 :
			l = [0, 0, 1, 1, 1]
			for x, i in enumerate(LED) :
				board.digital[i].write(l[x])
			
		elif LEVEL3 <= curve_value < LEVEL4 :
			l = [0, 0, 0, 1, 1]
			for x, i in enumerate(LED) :
				board.digital[i].write(l[x])

		elif LEVEL4 <= curve_value < LEVEL5 :
			l = [0, 0, 0, 0, 1]
			for x, i in enumerate(LED) :
				board.digital[i].write(l[x])

		elif LEVEL5 <= curve_value :
			for i in LED :
				board.digital[i].write(0)

	else :
		for i in LED :
			board.digital[i].write(0)
		exit()

