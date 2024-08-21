import time
import RPi.GPIO as GPIO


from subprocess import call
from pynput.keyboard import Key, Controller

try:
  from classes.pwmfan import Pwnfan
  from classes.remote import Remote
except ModuleNotFoundError:
  from pwmfan import Pwnfan
  from remote import Remote

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()

class Ignition:
  __IGN_LOW_TIME = 5
  __ignLowCounter = 0

  def __init__(self, ign_pin, remote_pin, fan_pin):
    self.__pin = ign_pin
    GPIO.setup(self.__pin, GPIO.IN)
    self.__remote = Remote(remote_pin)
    self.__remote.on()
    self.__fan = Pwnfan(fan_pin)
    print('ignition started')

  def main(self):
    self.__fan.main()
    if GPIO.input(self.__pin) != 1:
      self.__ignLowCounter += 1
      time.sleep(1)
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        print('shutting down')
        self.__remote.off()
        self.__keypress(Key.f12)
        time.sleep(5)
        call("sudo shutdown -h now", shell=True)
    else:
      self.__ignLowCounter = 0
      time.sleep(1)

  def __keypress(self, key):
    keycontroller.press(key)
    keycontroller.release(key)