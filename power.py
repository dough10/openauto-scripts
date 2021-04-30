import RPi.GPIO as GPIO
import time
from subprocess import call
from pynput.keyboard import Key, Controller

keycontroller = Controller()

GPIO.setmode(GPIO.BCM)

IGN_PIN = 17
EN_POWER_PIN = 25

IGN_LOW_TIME = 1

GPIO.setup(IGN_PIN, GPIO.IN)

GPIO.setup(EN_POWER_PIN, GPIO.OUT)

GPIO.output(EN_POWER_PIN, 1)

ignLowCounter = 0

def brightness(val):
	file = open("/sys/class/backlight/rpi_backlight/brightness","w")
	file.write(str(val))
	file.close()

brightness(255)

while 1:
	if GPIO.input(IGN_PIN) != 1:
		time.sleep(1)
		ignLowCounter += 1
		if ignLowCounter > IGN_LOW_TIME:
			brightness(5)
			print("Shutting Down")
			keycontroller.press(Key.f12)
			keycontroller.release(Key.f12)
			time.sleep(5)
			call("sudo shutdown -h now", shell=True)
	else:
		ignLowCounter = 0 
		time.sleep(1)
