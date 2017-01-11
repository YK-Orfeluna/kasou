# -*- coding: utf-8 -*

import wave, time
import pyfirmata, pyaudio
from config import *

DEBUG = True
#DEBUG = False



LEVEL_R = 0.5						# Thread-value of right-sensor
LEVEL_P = 0.1						# Thread-value of press-sensor

WAVE1 = ""							# wave-file's name
WAVE2 = ""
WAVE3 = ""
WAVE4 = ""
WAVE5 = ""
WAVE_DQ = ""
WAVE_DEAD = ""
WAVE = [WAVE1, WAVE2, WAVE3, WAVE4, WAVE5, WAVE_DQ, WAVE_DEAD]

audio_list = []
for i in xrange(len(WAVE)) :
	audio_list.append([])


CHUNK = 1024
OUTPUT = True

class App() :
	def __init__(self) :
		self.p = pyaudio.PyAudio()
		self.audio_list = audio_list

	def arduino_init(self) :
		self.board = pyfirmata.Arduino(PORT)			# Connect to Arduino

		it = pyfirmata.util.Iterator(self.board)		# Preparation to read Analog-pin
		it.start()

		self.curve = self.board.get_pin('a:%s:i' %CURVE)
		self.right = self.board.get_pin('a:%s:i' %RIGHT)
		self.press = self.board.get_pin('a:%s:i' %PRESS)

		print("Connect Arduino")

	def audio_init(self, name, i) :
		wf = wave.open(name, 'rb')
		self.audio_list[i][0].append(p.get_format_from_width(wf.getsampwidth()))	# ストリームを読み書きするときのデータ型
		self.audio_list[i][1].append(wf.getnchannels())								# ステレオかモノラルかの選択 1でモノラル 2でステレオ
		self.audio_list[i][2].append(wf.getframerate())								# サンプル周波数
		if DEBUG:
			print("%s: Audio init" %name)	

	def audio(name, i) :						# Play wave-file
		wf = wave.open(name, 'rb')
		stream = p.open(format=self.audio_list[i][0],			# ストリームを読み書きするときのデータ型
						channels=self.audio_list[i][1],			# ステレオかモノラルかの選択 1でモノラル 2でステレオ
						rate=self.audio_list[i][2],				# サンプル周波数
						output=OUTPUT)							# 出力モード

		data = wf.readframes(chunk)								# 1024個読み取り

		while data != '':
			stream.write(data)         							# ストリームへの書き込み(バイナリ)
			data = wf.readframes(chunk) 						# ファイルから1024個*2個の

		stream.stop_stream()
		stream.close()

		if DEBUG :
			print("Audio play")

	def digital_write(self, pin, value) :		# Write "HIGH" or "LOW"
		if value != 1 and value != 0 :
			sys.exit("function: digital_write\n2nd arg. is 1 or 0")
		self.board.digital[pin].write(value)

	def judge(self, name, num) :				# Kasou-Award
		for i in xrange(num) :
			self.digital_write(LED[i], 1)

		self.audio(name, num)

		for i in xrange(num) :
			self.digital_write(LED[i], 0)

		time.sleep(1)

	def main(self) :
		self.arduino_init()

		"""
		for i in xrange(len(WAVE)) :
			self.audio_init(WAVE[i])
		print("Audio init")
		"""

		print("System is Ready")

		while True :
			frameRate(30)

			curve_value = self.curve.read()		# Read value of curve-sensro
			right_value = self.right.read()		# Read value of right-sensor
			press_value = self.press.read()		# Read value of press-sensor

			if DEBUG :
				print("Sensor-Value, Curve - Right - Press : %s - %s - %s" %(curve_value, right_value, press_value)) 
			
			if True :
				for i in LED :
					self.digital_write(i, 1)
			else :
				for i in LED :
					self.digital_write(i, 0)

			"""
			if press_value > LEVEL_P :
				self.audio(WAVE_DQ, 5)

			if right_value < LEVEL_R :
				self.audio(WAVE_DEAD, 6)

			if LEVEL1 <= curve_value < LEVEL2:
				self.judge(WAVE1, 0)

			elif LEVEL2 <= curve_value < LEVEL3 :
				self.judge(WAVE2, 1)
				
			elif LEVEL3 <= curve_value < LEVEL4 :
				self.judge(WAVE3, 2)

			elif LEVEL4 <= curve_value < LEVEL5 :
				self.judge(WAVE4, 3)

			elif LEVEL5 <= curve_value :
				self.judge(WAVE5, 4)
			"""

if __name__ == "__main__" :
	app = App()
	app.main()
