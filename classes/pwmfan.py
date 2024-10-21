import subprocess

import RPi.GPIO as GPIO

from classes.logs import Logs

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs().get_logger()

class Pwnfan:
  def __init__(self, fan_pin:int) -> None:
    self.__pin = fan_pin
    GPIO.setup(self.__pin, GPIO.OUT)
    self.__fan = GPIO.PWM(self.__pin, 1000)
    self.__fan.start(0)
    logger.info('PWN started')

  def main(self) -> None:
    result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True)
    reading = result.stdout.split('=')[1].split("'")[0]
    if reading >= 75.0:
      self.__fan.ChangeDutyCycle(100.0)
    elif reading >= 70:
      self.__fan.ChangeDutyCycle(75.0)
    elif reading >= 65:
      self.__fan.ChangeDutyCycle(60.0)
    elif reading >= 60:
      self.__fan.ChangeDutyCycle(45.0)
    else:
      self.__fan.ChangeDutyCycle(30.0)