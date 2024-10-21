import time
from subprocess import call

import RPi.GPIO as GPIO
from pynput.keyboard import Key, Controller


try:
  from classes.pwmfan import Pwnfan
  from classes.remote import Remote
  from classes.logs import Logs
except ModuleNotFoundError:
  from pwmfan import Pwnfan
  from remote import Remote
  from logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()

logger = Logs().get_logger()

class Ignition:
  __IGN_LOW_TIME:int = 5
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, remote_pin:int, fan_pin:int) -> None:
    logger.info('ignition starting')
    self.__pin = ign_pin
    self.__remote = Remote(remote_pin)
    # self.__fan = Pwnfan(fan_pin)
    GPIO.setup(self.__pin, GPIO.IN)
    time.sleep(5)
    self.__remote.on()

  def __keypress(self, key:str) -> None:
    keycontroller.press(key)
    keycontroller.release(key)

  def main(self) -> None:
    # self.__fan.main()
    if GPIO.input(self.__pin) != 1:
      self.__ignLowCounter += 1
      time.sleep(1)
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        logger.info('shutting down')
        self.__remote.off()
        self.__keypress(Key.f12)
        time.sleep(5)
        call("sudo shutdown -h now", shell=True)
    else:
      self.__ignLowCounter = 0
      time.sleep(1)