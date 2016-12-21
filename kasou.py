# -*- coding: utf-8 -*

import wave, time
import pyfirmata, pyaudio

#DEBUG = True
DEBUG = False

PORT = ""							# Arduino port: ls /dev/cu*

SENSOR = 0							# SENSOR position in Analog pin

LEVEL1 = 0
LEVEL2 = 0
LEVEL3 = 0
LEVEL4 = 0
LEVEL5 = 0

LED1 = 0							# LED position in Digital pin
LED2 = 0
LED3 = 0
LED4 = 0
LED5 = 0
LED = [LED1, LED2,LED3, LED4, LED5]

WAVE1 = ""
WAVE2 = ""
WAVE3 = ""
WAVE4 = ""
WAVE5 = ""
WAVE = [WAVE1, WAVE2, WAVE3, WAVE4, WAVE5]

CHUNK = 1024
OUTPUT = True

class App() :
	def __init__(self) :
		self.p = pyaudio.PyAudio()
		self.audio_list = [[], [], [], [], []]

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
						channels=self.audio_list[i][1],		# ステレオかモノラルかの選択 1でモノラル 2でステレオ
						rate=self.audio_list[i][2],				# サンプル周波数
						output=OUTPUT)					# 出力モード

		data = wf.readframes(chunk)						# 1024個読み取り

		while data != '':
			stream.write(data)         					# ストリームへの書き込み(バイナリ)
			data = wf.readframes(chunk) 				# ファイルから1024個*2個の

		stream.stop_stream()
		stream.close()

		if INFO :
			print("step!")

	def sensor_read(pin) :				# Read value in Analog pin
		out = self.board.analog[pin].read
		return out

	def digital_write(pin, value) :		# Write "HIGH" or "LOW"
		if value != 1 and value != 0
			sys.exit("function: digital_write\n2nd arg. is 1 or 0")
		self.board.digital[pin].write(value)

	def judge(self, name, num) :
		for i in xrange(num) :
			self.digital_write(LED[i], 1)

		self.audio(name)

		for i in xrange(num) :
			self.digital_write(LED[i], 0)

		time.sleep(1)

	def main(self) :
		self.board = pyfirmata.Arduino(PORT)		# Connect Arduino
		print("Connect Arduino")

		for i in xrange(len(WAVE))
			self.audio_init(WAVE[i])
		print("Audio init")

		while True :
			value = self.sensor_read(SENSOR)

			if LEVEL1 <= value < LEVEL2:
				self.judge(WAVE1)

			elif LEVEL2 <= value < LEVEL3 :
				self.judge(WAVE2)
				
			elif LEVEL3 <= value < LEVEL4 :
				self.judge(WAVE3)

			elif LEVEL4 <= value < LEVEL5 :
				self.judge(WAVE4)

			elif LEVEL5 <= value :
				self.judge(WAVE5)
