import time
from subprocess import call

import RPi.GPIO as GPIO
from pynput import keyboard
from pynput.keyboard import Controller

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()


from classes.logs import Logs
logger = Logs(__file__).get_logger()

from classes.pwmfan import Pwnfan
from classes.remote import Remote


class Ignition:
  __IGN_LOW_TIME:int = 3
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, remote_pin:int, fan_pin:int, fan_speed_pin:int, latch_pin:int) -> None:
    logger.info(f'Starting {__file__}')
    logger.debug(f'ignotion pin:{ign_pin}, remote pin:{remote_pin}, fan pin:{fan_pin}, latch pin:{latch_pin}')
    self.__pin = ign_pin
    self.__remote = Remote(remote_pin)
    self.__fan = Pwnfan(fan_pin, fan_speed_pin)
    GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(latch_pin, GPIO.OUT)
    time.sleep(3) # give time for system to complete boot before turning on remote
    self.__remote.on()
    GPIO.output(latch_pin, 1)
    logger.info('latch on')

  def __keypress(self, key:str) -> None:
    keycontroller.press(key)
    keycontroller.release(key)

  def main(self) -> None:
    self.__fan.main()
    state = GPIO.input(self.__pin)
    logger.debug(f'ign pin state: {state}')
    if state != 1:
      self.__ignLowCounter += 1
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        logger.info('shutting down')
        self.__keypress(keyboard.Key.f12)
        self.__remote.off() # shut off remote to reduce chance of pop or noise as system shuts down
        time.sleep(2) # leave enough time for volume to fully reset
        self.__remote.cleanup()
        self.__fan.cleanup()
        call("sudo shutdown -h now", shell=True)
        return
    else:
      self.__ignLowCounter = 0
    time.sleep(1)
    


if __name__ == "__main__":
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  
  IGN_PIN = os.getenv('IGN_PIN') or 17
  REMOTE_PIN = os.getenv('REMOTE_PIN') or 25
  FAN_PIN = os.getenv('FAN_PIN') or 12
  LATCH_PIN = os.getenv('LATCH_PIN') or 4
  FAN_SPEED_PIN = os.getenv('FAN_SPEED_PIN') or 24

  ignition = Ignition(IGN_PIN, REMOTE_PIN, FAN_PIN, FAN_SPEED_PIN, LATCH_PIN)

  try:
    while True:
      ignition.main()
  except Exception as e:
    logger.exception("main crashed. Error: %s", e) 
    exit()