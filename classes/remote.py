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
    self.__pin = pin
    GPIO.setup(self.__pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

  def on(self) -> None:
    GPIO.output(self.__pin, 1)
    logger.info('Remote on')

  def off(self) -> None:
    GPIO.output(self.__pin, 0)
    logger.info('remote off')
