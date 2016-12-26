# -*- coding: utf-8 -*

import time

PORT = "/dev/cu.usbmodem1411"		# Arduino port: ls /dev/cu*

CURVE = 5							# Curve-sensor position in Analog-pin
RIGHT = 4							# Right-sensor position in Analog-pin
PRESS = 3							# Press-sensor position in Analog-pin

LED1 = 2							# LED position in Digital-pin
LED2 = 4
LED3 = 6
LED4 = 8
LED5 = 10
LED = [LED1, LED2,LED3, LED4, LED5]

LEVEL1 = 0.1							# Thread-value of curve-sensor
LEVEL2 = 0.15
LEVEL3 = 0.2
LEVEL4 = 0.25
LEVEL5 = 0.3

def frameRate(fps) :							# Config of framerate
	ms = round(1000.0 / fps, 0)					# Between-time of frame(mill-second)
	s = ms / 1000.0								# Between-time of frame(second)
	time.sleep(s)
