import subprocess
from typing import List, Tuple

import RPi.GPIO as GPIO

try:
  from classes.logs import Logs
  from classes.debounce import debounce
except ModuleNotFoundError:
  from debounce import debounce
  from logs import Logs


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = Logs(__file__).get_logger()

class Pwnfan:
  def __init__(self, fan_pin:int, duty_cycles:List[Tuple[float, float]], default_duty: float = 20.0) -> None:
    logger.info(f'Starting {__file__}')
    self.__duty_cycles = duty_cycles
    self.__default_duty = default_duty
    self.__pin = fan_pin
    GPIO.setup(self.__pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
    self.__fan = GPIO.PWM(self.__pin, 1000)
    self.__fan.start(0)

  @debounce(30)
  def main(self) -> None:
    try:
      result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
      reading = float(result.stdout.split('=')[1].split("'")[0])
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
      logger.error(f"Error reading temperature: {e}")
      return

    for threshold, duty in self.__duty_cycles:
      if reading >= threshold:
        self.__fan.ChangeDutyCycle(duty)
        logger.info(f"Fan speed adjusted to {duty}% for temperature {reading}°C")
        return

    self.__fan.ChangeDutyCycle(self.__default_duty)
    logger.info(f"Fan speed set to {self.__default_duty}% (default)")

  def cleanup(self) -> None:
    self.__fan.stop()
    GPIO.cleanup()


if __name__ == "__main__":
  # GPIO pin number
  pin = 12
  # (temperature threshold, fan speed precentage)
  duty_cycles = [
    (75.0, 100.0),
    (70.0, 85.0),
    (65.0, 70.0),
    (60.0, 55.0),
    (50.0, 45.0),
    (40.0, 35.0),
    (30.0, 30.0),
    (20.0, 0.0)
  ]
  fan = Pwnfan(pin, duty_cycles)
  
  try:
    while True:
      fan.main()
  except KeyboardInterrupt:
    fan.cleanup()