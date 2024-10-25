import time
from subprocess import call

import RPi.GPIO as GPIO
from pynput import keyboard
from pynput.keyboard import Controller


from classes.pwmfan import Pwnfan
from classes.remote import Remote
from classes.logs import Logs


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


keycontroller = Controller()
logger = Logs().get_logger()


class Ignition:
  __IGN_LOW_TIME:int = 3
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, remote_pin:int, fan_pin:int, latch_pin:int) -> None:
    logger.info('Starting power.py')
    logger.info(f'ignotion pin:{ign_pin}, remote pin:{remote_pin}, fan pin:{fan_pin}, latch pin:{latch_pin}')
    self.__pin = ign_pin
    self.__latch_pin = latch_pin
    self.__remote = Remote(remote_pin)
    self.__fan = Pwnfan(fan_pin)
    GPIO.setup(self.__pin, GPIO.IN)
    GPIO.setup(self.__latch_pin, GPIO.OUT)
    time.sleep(2)
    self.__remote.on()
    GPIO.output(self.__latch_pin, 1)
    logger.info(f'latch on')

  def __keypress(self, key:str) -> None:
    keycontroller.press(key)
    keycontroller.release(key)

  def main(self) -> None:
    self.__fan.main()
    if GPIO.input(self.__pin) != 1:
      self.__ignLowCounter += 1
      time.sleep(1)
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        logger.info('shutting down')
        self.__remote.off()
        self.__keypress(keyboard.Key.f12)
        time.sleep(1)
        call("sudo shutdown -h now", shell=True)
    else:
      self.__ignLowCounter = 0
      time.sleep(1)


if __name__ == "__main__":
  IGN_PIN = 17
  REMOTE_PIN = 25
  FAN_PIN = 12
  LATCH_PIN = 4

  ignition = Ignition(IGN_PIN, REMOTE_PIN, FAN_PIN, LATCH_PIN)

  try:
    while True:
      ignition.main()
  except Exception as e:
    logger.exception("main crashed. Error: %s", e) 
