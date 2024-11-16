import time
from subprocess import call

import RPi.GPIO as GPIO
from pynput import keyboard
from pynput.keyboard import Controller

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()


from classes.logs import Logs
logger = Logs().get_logger()

from classes.pwmfan import Pwnfan
from classes.remote import Remote


class Ignition:
  __IGN_LOW_TIME:int = 3
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, remote_pin:int, fan_pin:int, fan_speed_pin:int, latch_pin:int) -> None:
    logger.info(f'Starting {__file__}, IGN_PIN:{ign_pin}, LATCH_PIN:{latch_pin}')
    self.__pin = ign_pin
    self.__remote = Remote(remote_pin)
    self.__fan = Pwnfan(fan_pin, fan_speed_pin)
    GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(latch_pin, GPIO.OUT)
    time.sleep(3) # give time for system to complete boot before turning on remote
    self.__remote.on()
    try:
      GPIO.output(latch_pin, GPIO.HIGH)
      logger.info('latch on')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {latch_pin} high: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")

  def __keypress(self, key:str) -> None:
    keycontroller.press(key)
    keycontroller.release(key)
    logger.debug('F12 keypress fired')

  def main(self) -> None:
    self.__fan.main()
    state = GPIO.input(self.__pin)
    if state != GPIO.HIGH:
      logger.debug(f'ign pin state: {state}')
      self.__ignLowCounter += 1
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        self.__keypress(keyboard.Key.f12)
        self.__remote.off() # shut off remote to reduce chance of pop or noise as system shuts down
        time.sleep(2) # leave enough time for volume to fully reset
        self.__remote.cleanup()
        self.__fan.cleanup()
        logger.info('shutting down')
        call("sudo shutdown -h now", shell=True)
        return
    else:
      self.__ignLowCounter = 0
    time.sleep(1)
    


if __name__ == "__main__":
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  
  IGN_PIN = int(os.getenv('IGN_PIN', 17))
  LATCH_PIN = int(os.getenv('LATCH_PIN', 4))
  REMOTE_PIN = int(os.getenv('REMOTE_PIN', 25))
  FAN_PIN = int(os.getenv('FAN_PIN', 12))
  FAN_SPEED_PIN = int(os.getenv('FAN_SPEED_PIN', 24))

  ignition = Ignition(IGN_PIN, REMOTE_PIN, FAN_PIN, FAN_SPEED_PIN, LATCH_PIN)

  try:
    while True:
      ignition.main()
  except Exception as e:
    logger.exception("main crashed. Error: %s", e) 
    exit()