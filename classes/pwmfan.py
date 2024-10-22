import subprocess

import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs().get_logger()

class Pwnfan:
  def __init__(self, fan_pin:int) -> None:
    self.__pin = fan_pin
    GPIO.setup(self.__pin, GPIO.OUT)
    self.__fan = GPIO.PWM(self.__pin, 1000)
    self.__fan.start(0)

  def main(self) -> None:
    result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True)
    reading = float(result.stdout.split('=')[1].split("'")[0])
    logger.info(reading)
    duty_cycles = [
        (75.0, 100.0),
        (70.0, 75.0),
        (65.0, 60.0),
        (60.0, 45.0)
    ]

    for threshold, duty in duty_cycles:
        if reading >= threshold:
            self.__fan.ChangeDutyCycle(duty)
            return

    self.__fan.ChangeDutyCycle(30.0)
      

if __name__ == "__main__":
  fan = Pwnfan(18)
  while True:
    fan.main()  