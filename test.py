import RPi.GPIO as GPIO
from gpiozero import CPUTemperature
import time


cpu = CPUTemperature()

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

FAN_PIN = 18

GPIO.setup(FAN_PIN, GPIO.OUT)

fan = GPIO.PWM(FAN_PIN,1000)
fan.start(0)


while 1:
    print(cpu.temperature)
    if cpu.temperature >= 61.0:
        fan.ChangeDutyCycle(100.0)
    else:
        fan.ChangeDutyCycle(10.0)
    time.sleep(10)