import RPi.GPIO as GPIO
import time
from gpiozero import CPUTemperature
from subprocess import call
from pynput.keyboard import Key, Controller

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

keycontroller = Controller()

IGN_PIN = 17
REMOTE_PIN = 25
FAN_PIN = 18

# monitor CPU temperature 
class Pwnfan:
	def __init__(self, fan_pin):
		self.__pin = fan_pin
		self.__cpu = CPUTemperature()
		GPIO.setup(self.__pin, GPIO.OUT)
		self.__fan = GPIO.PWM(self.__pin, 1000)
		self.__fan.start(0)
		print('PWN started')

	def getCPUTemp(self):
		reading = self.__cpu.temperature
		if reading >= 75.0:
			self.__fan.ChangeDutyCycle(100.0)
		elif reading >= 70:
			self.__fan.ChangeDutyCycle(75.0)
		elif reading >= 65:
			self.__fan.ChangeDutyCycle(60.0)
		elif reading >= 60:
			self.__fan.ChangeDutyCycle(45.0)
		else:
			self.__fan.ChangeDutyCycle(30.0)

# remote turn on 
class Remote:
	def __init__(self, pin):
		self.__pin = pin
		GPIO.setup(self.__pin, GPIO.OUT)
		print('remote started')

	def on(self):
		GPIO.output(self.__pin, 1)
		print('Remote on')

	def off(self):
		GPIO.output(self.__pin, 0)
		print('remote off')

# 
class Ignition:
	__IGN_LOW_TIME = 3
	__ignLowCounter = 0

	def __init__(self, ign_pin, remote_pin):
		self.__pin = ign_pin
		GPIO.setup(self.__pin, GPIO.IN)
		self.__remote = Remote(remote_pin)
		self.__remote.on()
		print('ignition started')

	def isRunning(self):
		if GPIO.input(self.__pin) != 1:
			self.__ignLowCounter += 1
			time.sleep(1)
			if self.__ignLowCounter >= self.__IGN_LOW_TIME:
				print('shutting down')
				self.__keypress(Key.f12)
				time.sleep(5)
				self.__remote.off()
				call("sudo shutdown -h now", shell=True)
		else:
			self.__ignLowCounter = 0
			time.sleep(1)

	def __keypress(self, key):
		keycontroller.press(key)
		keycontroller.release(key)

ignition = Ignition(IGN_PIN, REMOTE_PIN)
fan = Pwnfan(FAN_PIN)

while True:
	fan.getCPUTemp()
	ignition.isRunning()
