import time
from typing import Callable
from subprocess import call
import RPi.GPIO as GPIO
from pynput import keyboard
from pynput.keyboard import Controller

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
keycontroller = Controller()

try:
  from classes.logs import Logs
  from classes.debounce import debounce
except ModuleNotFoundError:
  from debounce import debounce
  from logs import Logs

logger = Logs().get_logger()


class Ignition:
  """
  The Ignition class controls the startup and shutdown process of a system.
  It interacts with hardware components such as GPIO pins, a remote control,
  and a PWM fan, as well as triggering system shutdown procedures.

  Attributes:
    __IGN_LOW_TIME (int): Threshold time (in seconds) for low ignition state to trigger shutdown.
    __ignLowCounter (int): Counter for tracking consecutive ignition pin low states.
    __pin (int): GPIO pin used to monitor ignition state (e.g., car ignition signal).
  """
  __ignLowCounter:int = 0

  def __init__(self, ign_pin:int, latch_pin:int, ign_low_time:int, external_options:Callable[[], None]) -> None:
    """
    Initializes the Ignition object and sets up GPIO pins and devices.
    
    Args:
      ign_pin (int): GPIO pin number connected to the ignition signal.
      latch_pin (int): GPIO pin used for the latch power control.
      ign_low_time (int): time to wait before shutdown code is ran
      external_options (function): additional methods that need to be executed before shutdown
    """
    logger.info(f'IGN_PIN:{ign_pin}, LATCH_PIN:{latch_pin}')
    self.__IGN_LOW_TIME = ign_low_time
    self.__pin = ign_pin
    self.__external_options = external_options
    GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.__latch_power(latch_pin)

  def __keypress(self, key:str) -> None:
    """
    Simulates a key press event.

    Args:
      key (str): The key to be pressed.
    """
    keycontroller.press(key)
    keycontroller.release(key)

  def __latch_power(self, latch_pin:int) -> None:
    """
    Controls the latch power (GPIO output).
    
    Sets the latch pin to HIGH, turning on power that will keep a relay closed until system shutdown.

    Args:
      latch_pin (int): GPIO pin controlling the power latch.
    """
    GPIO.setup(latch_pin, GPIO.OUT)
    try:
      GPIO.output(latch_pin, GPIO.HIGH)
      logger.info('LATCH_PIN: HIGH')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {latch_pin} high: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")
      
  @debounce(30)
  def __shutdown(self) -> None:
    """
    Perform the shutdown process
    
    The function also manages the fan dashcam and remote control states.

    The shutdown process includes:
    - Pressing the F12 key (e.g., to trigger volume normalization)
    - Stops dashcam recording
    - Turning off the remote device
    - Shutting down the system via a shell command
    """
    self.__keypress(keyboard.Key.f12)
    if self.__external_options:
      self.__external_options()
    logger.info('shutting down')
    call("sudo shutdown -h now", shell=True) 
      
  def main(self) -> None:
    """
    Main loop that continuously checks the ignition state and triggers shutdown 
    if the ignition state is low for more than the defined threshold time.
    """
    state = GPIO.input(self.__pin)
    if state != GPIO.HIGH:
      logger.debug(f'IGN_PIN state: {state}, __ignLowCounter: {self.__ignLowCounter}')
      self.__ignLowCounter += 1
      if self.__ignLowCounter >= self.__IGN_LOW_TIME:
        self.__shutdown()
    else:
      self.__ignLowCounter = 0
    
    
if __name__ == "__main__":
  IGN_PIN = 17
  LATCH_PIN = 4
  IGN_LOW_TIME = 3


  ignition = Ignition(IGN_PIN, LATCH_PIN, IGN_LOW_TIME)

  try:
    while True:
      ignition.main()
      time.sleep(1)
  except Exception as e:
    logger.exception("main crashed. Error: %s", e) 
    exit()