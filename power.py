import RPi.GPIO as GPIO
import time
from subprocess import call
from pynput.keyboard import Key, Controller

keycontroller = Controller()

GPIO.setmode(GPIO.BCM)

IGN_PIN = 17
REMOTE_PIN = 25
FAN_PIN = 18

IGN_LOW_TIME = 5

GPIO.setup(IGN_PIN, GPIO.IN)

GPIO.setup(REMOTE_PIN, GPIO.OUT)

GPIO.output(REMOTE_PIN, 1)

GPIO.setup(FAN_PIN, GPIO.OUT)

fan = GPIO.PWN(FAN_PIN,1000)
fan.start(0)

ignLowCounter = 0

def temp():
	return call('cat /sys/class/thermal/thermal_zone0/temp', shell=True)

def brightness(val):
	file = open("/sys/class/backlight/rpi_backlight/brightness","w")
	file.write(str(val))
	file.close()

def keypress(key):
	keycontroller.press(key)
	keycontroller.release(key)

brightness(255)

while 1:
	if GPIO.input(IGN_PIN) != 1:
		time.sleep(1)
		ignLowCounter += 1
		if ignLowCounter > IGN_LOW_TIME:
			brightness(5)
			print("Shutting Down")
			keypress(Key.f12)
			time.sleep(5)
			GPIO.output(REMOTE_PIN, 0)
			call("sudo shutdown -h now", shell=True)
	else:
		ignLowCounter = 0
		time.sleep(1)
