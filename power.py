import os
import time
from subprocess import call
from dotenv import load_dotenv

import RPi.GPIO as GPIO
from pynput import keyboard
from pynput.keyboard import Controller

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()

load_dotenv()

from classes.logs import Logs
logger = Logs().get_logger()

from classes.pwmfan import Pwmfan
from classes.remote import Remote


class Ignition:
  """
  The Ignition class controls the startup and shutdown process of a system.
  It interacts with hardware components such as GPIO pins, a remote control,
  and a PWM fan, as well as triggering system shutdown procedures.

  Attributes:
    IGN_LOW_TIME (int): Threshold time (in seconds) for low ignition state to trigger shutdown.
    __ignLowCounter (int): Counter for tracking consecutive ignition pin low states.
    __pin (int): GPIO pin used to monitor ignition state (e.g., car ignition signal).
    __remote (Remote): Remote control instance for handling remote power state.
    __fan (Pwmfan): PWM fan instance for controlling fan state.
  """
  IGN_LOW_TIME:int = int(os.getenv('IGN_LOW_TIME', 3))
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, remote_pin:int, fan_pin:int, fan_speed_pin:int, latch_pin:int) -> None:
    """
    Initializes the Ignition object and sets up GPIO pins and devices.
    
    Args:
      ign_pin (int): GPIO pin number connected to the ignition signal.
      remote_pin (int): GPIO pin connected to the remote control.
      fan_pin (int): GPIO pin connected to the fan.
      fan_speed_pin (int): GPIO pin connected to the fan speed tachometer.
      latch_pin (int): GPIO pin used for the latch power control.
    """
    logger.info(f'Starting {__file__}, IGN_PIN:{ign_pin}, LATCH_PIN:{latch_pin}')
    self.__pin = ign_pin
    self.__remote = Remote(remote_pin)
    self.__fan = Pwmfan(fan_pin, fan_speed_pin)
    GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.__latch_power(latch_pin)
    time.sleep(3) # give time for system to complete boot before turning on remote
    self.__remote.on()

  def __keypress(self, key:str) -> None:
    """
    Simulates a key press event.

    Args:
      key (str): The key to be pressed.
    """
    keycontroller.press(key)
    keycontroller.release(key)
    logger.debug('F12 keypress fired')

  def __latch_power(self, latch_pin) -> None:
    """
    Controls the latch power (GPIO output).
    
    Sets the latch pin to HIGH, turning on power that will keep a relay closed until system shutdown.

    Args:
      latch_pin (int): GPIO pin controlling the power latch.
    """
    GPIO.setup(latch_pin, GPIO.OUT)
    try:
      GPIO.output(latch_pin, GPIO.HIGH)
      logger.info('power latch: on')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {latch_pin} high: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")
      
  def main(self) -> None:
    """
    Main loop that continuously checks the ignition state and triggers shutdown 
    if the ignition state is low for more than the defined threshold time.
    
    The function also manages the fan and remote control states.

    The shutdown process includes:
    - Pressing the F12 key (e.g., to trigger volume normalization)
    - Turning off the remote device
    - Shutting down the system via a shell command
    """
    self.__fan.main()
    state = GPIO.input(self.__pin)
    if state != GPIO.HIGH:
      logger.debug(f'IGN_PIN state: {state}, __ignLowCounter: {self.__ignLowCounter}')
      self.__ignLowCounter += 1
      if self.__ignLowCounter >= self.IGN_LOW_TIME:
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