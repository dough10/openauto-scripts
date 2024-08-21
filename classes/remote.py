import RPi.GPIO as GPIO

from classes.logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs().get_logger()

class Remote:
  def __init__(self, pin) -> None:
    self.__pin = pin
    GPIO.setup(self.__pin, GPIO.OUT)
    logger.info('remote started')

  def on(self) -> None:
    GPIO.output(self.__pin, 1)
    logger.info('Remote on')

  def off(self) -> None:
    GPIO.output(self.__pin, 0)
    logger.info('remote off')
