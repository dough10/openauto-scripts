import subprocess
import time
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
  # (temperature threshold, fan speed precentage)
  __duty_cycles:List[Tuple[float, float]] = [
    (75.0, 100.0),
    (70.0, 85.0),
    (65.0, 70.0),
    (60.0, 55.0),
    (50.0, 45.0),
    (40.0, 35.0),
    (30.0, 30.0)
  ]  
  __default_duty:float = 25.0
  __t = time.time()
  __pulse:int = 2
  __frequency:int = 25000
  
  rpm:int = 0
  
  def __init__(self, fan_pin:int, speed_pin:int) -> None:
    logger.info(f'Starting {__file__}')
    GPIO.setup(speed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(speed_pin, GPIO.FALLING, self.__fell)
    GPIO.setup(fan_pin, GPIO.OUT)
    self.__fan = GPIO.PWM(fan_pin, self.__frequency)
    self.__fan.start(0)
    
  @debounce(30)
  def main(self) -> None:
    try:
      result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
      logger.error(f"Error reading temperature: {e}")
      return

    reading_c = float(result.stdout.split('=')[1].split("'")[0])
    reading_f = round(((reading_c * 9) / 5) + 32, 1)
    
    for threshold, duty in self.__duty_cycles:
      if reading_c >= threshold:
        self.__fan.ChangeDutyCycle(duty)
        logger.info(f"Fan speed ({self.rpm}rpm) adjusted to {duty}% for temperature {reading_c}°C ({reading_f}°F)")
        self.rpm = 0
        return

    self.__fan.ChangeDutyCycle(self.__default_duty)
    logger.info(f"Fan speed ({self.rpm}rpm) set to {self.__default_duty}% (default) for temperature {reading_c}°C ({reading_f}°F)")
    self.rpm = 0

  def cleanup(self) -> None:
    self.__fan.stop()
    GPIO.cleanup()

  def __fell(self, n) -> None:
    logger.debug(f'fell: {n}')
    dt = time.time() - self.__t
    if dt < 0.005: return

    freq = 1 / dt
    self.rpm = (freq / self.__pulse) * 60
    self.__t = time.time()


if __name__ == "__main__":
  # GPIO pin number
  fan_pin = 12
  fan_tach = 24
  
  fan = Pwnfan(fan_pin, fan_tach)
  
  try:
    while True:
      fan.main()
  except KeyboardInterrupt:
    fan.cleanup()