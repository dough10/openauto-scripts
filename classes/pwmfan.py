import RPi.GPIO as GPIO
import logging
from gpiozero import CPUTemperature

logging.basicConfig(level=logging.warning)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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