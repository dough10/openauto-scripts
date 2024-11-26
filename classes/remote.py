import os
import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs().get_logger()

class Remote:
  """
  A class to control a remote device connected to a GPIO pin on a Raspberry Pi.
  
  The `Remote` class allows the user to turn a remote device on and off by setting
  a specified GPIO pin to either HIGH (on) or LOW (off). It also includes cleanup functionality
  to reset the GPIO state when finished.
  """
  def __init__(self, pin:int) -> None:
    """
    Initialize the Remote object and configure the GPIO pin.
    
    Args:
      pin (int): The GPIO pin number connected to the remote device (e.g., relay or switch).
    """
    logger.info(f'REMOTE_PIN:{pin}')
    self.__pin:int = pin
    GPIO.setup(self.__pin, GPIO.OUT)

  def on(self) -> None:
    """
    Turn the remote device on by setting the GPIO pin to HIGH.
    
    If there is an error in setting the pin, it will be logged.
    """
    try:
      GPIO.output(self.__pin, GPIO.HIGH)
      logger.info('REMOTE_PIN: HIGH')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {self.__pin} high: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")

  def off(self) -> None:
    """
    Turn the remote device off by setting the GPIO pin to LOW.
    
    If there is an error in setting the pin, it will be logged.
    """
    try:
      GPIO.output(self.__pin, GPIO.LOW)
      logger.info('REMOTE_PIN: LOW')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {self.__pin} low: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")
    
  def cleanup(self) -> None:
    """
    Clean up the GPIO setup when the script finishes or when no longer needed.
    
    This resets all the GPIO settings, ensuring no conflicting states remain.
    """
    GPIO.cleanup()
    logger.info("GPIO cleaned up")