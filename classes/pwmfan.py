import subprocess

import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
  from classes.debounce import debounce
except ModuleNotFoundError:
  from debounce import debounce
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

  @debounce(30)
  def main(self) -> None:
    result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True)
    reading = float(result.stdout.split('=')[1].split("'")[0])
    logger.info(f"Temperature reading: {reading}")

    duty_cycles = [
      (75.0, 100.0),
      (70.0, 85.0),
      (65.0, 70.0),
      (60.0, 55.0),
      (50.0, 45.0),
      (40.0, 35.0),
      (30.0, 30.0)
    ]

    for threshold, duty in duty_cycles:
      if reading >= threshold:
        self.__fan.ChangeDutyCycle(duty)
        logger.info(f"Fan speed adjusted to {duty}% for temperature {reading}°C")
        return

    self.__fan.ChangeDutyCycle(20.0)
    logger.info("Fan speed set to 20% (default)")
      

if __name__ == "__main__":
  fan = Pwnfan(18)
  while True:
    fan.main()  