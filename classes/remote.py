import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs().get_logger()

class Remote:
  def __init__(self, pin) -> None:
    logger.info(f'Starting {__file__}, REMOTE_PIN:{pin}')
    self.__pin = pin
    GPIO.setup(self.__pin, GPIO.OUT)

  def on(self) -> None:
    try:
      GPIO.output(self.__pin, GPIO.HIGH)
      logger.info('Remote turn on: on')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {self.__pin} high: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")

  def off(self) -> None:
    try:
      GPIO.output(self.__pin, GPIO.LOW)
      logger.info('Remote turn on: off')
    except GPIO.error as e:
      logger.error(f"Error setting GPIO pin {self.__pin} low: {e}")
    except Exception as e:
      logger.critical(f"Unexpected error: {e}")
    
  def cleanup(self) -> None:
    GPIO.cleanup()
    logger.info("GPIO cleaned up")