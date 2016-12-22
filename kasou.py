# -*- coding: utf-8 -*

import wave, time
import pyfirmata, pyaudio

#DEBUG = True
DEBUG = False

PORT = ""							# Arduino port: ls /dev/cu*

CURVE = 0							# Curve-sensor position in Analog-pin
RIGHT = 0							# Right-sensor position in Analog-pin
SWITCH = 0							# Switch position in Digital-pin

LEVEL1 = 0							# Thread of curve-sensor-value
LEVEL2 = 0
LEVEL3 = 0
LEVEL4 = 0
LEVEL5 = 0

LEVEL_R = 0							# Thread of right-sensor-value

LED1 = 0							# LED position in Digital-pin
LED2 = 0
LED3 = 0
LED4 = 0
LED5 = 0
LED = [LED1, LED2,LED3, LED4, LED5]

WAVE1 = ""							# wave-file's name
WAVE2 = ""
WAVE3 = ""
WAVE4 = ""
WAVE5 = ""
WAVE_DQ = ""
WAVE_DEAD = ""
WAVE = [WAVE1, WAVE2, WAVE3, WAVE4, WAVE5, WAVE_DQ, WAVE_DEAD]

CHUNK = 1024
OUTPUT = True

class App() :
	def __init__(self) :
		self.p = pyaudio.PyAudio()
		self.audio_list = [[], [], [], [], [], [], []]

	def audio_init(self, name, i) :				# 足音wavの情報を保存する
		wf = wave.open(name, 'rb')
		self.audio_list[i][0].append(p.get_format_from_width(wf.getsampwidth()))	# ストリームを読み書きするときのデータ型
		self.audio_list[i][1].append(wf.getnchannels())							# ステレオかモノラルかの選択 1でモノラル 2でステレオ
		self.audio_list[i][2].append(wf.getframerate())							# サンプル周波数
		if DEBUG:
			print("%s: Audio init" %name)	

	def audio(name, i) :						# 音を鳴らす
		wf = wave.open(name, 'rb')
		stream = p.open(format=self.audio_list[i][0],			# ストリームを読み書きするときのデータ型
						channels=self.audio_list[i][1],			# ステレオかモノラルかの選択 1でモノラル 2でステレオ
						rate=self.audio_list[i][2],				# サンプル周波数
						output=OUTPUT)						# 出力モード

		data = wf.readframes(chunk)								# 1024個読み取り

		while data != '':
			stream.write(data)         							# ストリームへの書き込み(バイナリ)
			data = wf.readframes(chunk) 						# ファイルから1024個*2個の

		stream.stop_stream()
		stream.close()

		if INFO :
			print("step!")

	def digital_write(pin, value) :		# Write "HIGH" or "LOW"
		if value != 1 and value != 0 :
			sys.exit("function: digital_write\n2nd arg. is 1 or 0")
		self.board.digital[pin].write(value)

	def judge(self, name, num) :
		for i in xrange(num) :
			self.digital_write(LED[i], 1)

		self.audio(name, num)

		for i in xrange(num) :
			self.digital_write(LED[i], 0)

		time.sleep(1)

	def main(self) :
		self.board = pyfirmata.Arduino(PORT)		# Connect Arduino
		print("Connect Arduino")

		for i in xrange(len(WAVE)) :
			self.audio_init(WAVE[i])
		print("Audio init")

		print("System is Ready")

		while True :
			curve_value = self.board.analog[CURVE].read		# Read curve-sensor-value
			right_value = self.board.analog[RIGHT].read		# Read right-sensor-value
			s = self.self.board.digital[Switch].read		# Read Switch-value

			if s == 1 :
				self.audio(WAVE_DQ)

			if right_value < LEVEL_R :
				self.audio(WAVE_DEAD)

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
