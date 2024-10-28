import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs(__file__).get_logger()

class Remote:
  def __init__(self, pin) -> None:
    logger.info(f'Starting {__file__}')
    self.__pin = pin
    GPIO.setup(self.__pin, GPIO.OUT)

  def on(self) -> None:
    GPIO.output(self.__pin, 1)
    logger.info('Remote on')

  def off(self) -> None:
    GPIO.output(self.__pin, 0)
    logger.info('remote off')
    
  def cleanup(self) -> None:
    GPIO.cleanup()
    logger.info("GPIO cleaned up")