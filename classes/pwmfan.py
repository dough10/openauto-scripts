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
  def __init__(self, fan_pin:int, speed_pin:int) -> None:
    logger.info(f'Starting {__file__}')
    
    # fan pulse per second
    self.rpm:int = 0
    self.__t = time.time()
    self.__pulse:int = 2
    self.__frequency:int = 25000
    self.__default_duty:float = 20.0
    # (temperature threshold, fan speed precentage)
    self.__duty_cycles:List[Tuple[float, float]] = [
      (75.0, 100.0),
      (70.0, 85.0),
      (65.0, 70.0),
      (60.0, 55.0),
      (50.0, 45.0),
      (40.0, 35.0),
      (30.0, 30.0)
    ]   
    
    GPIO.setup(fan_pin, GPIO.OUT)
    self.__fan = GPIO.PWM(fan_pin, self.__frequency)
    self.__fan.start(0)
    GPIO.setup(speed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(speed_pin, GPIO.FALLING, self.__fell)
    

  @debounce(30)
  def main(self) -> None:
    try:
      result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
      logger.error(f"Error reading temperature: {e}")
      return

    reading = float(result.stdout.split('=')[1].split("'")[0])
    
    for threshold, duty in self.__duty_cycles:
      if reading >= threshold:
        self.__fan.ChangeDutyCycle(duty)
        logger.info(f"Fan speed ({self.rpm}rpm) adjusted to {duty}% for temperature {reading}°C")
        return

    self.__fan.ChangeDutyCycle(self.__default_duty)
    logger.info(f"Fan speed ({self.rpm}rpm) set to {self.__default_duty}% (default)")

  def cleanup(self) -> None:
    self.__fan.stop()
    GPIO.cleanup()

  def fell(self, n):
    dt = time.time() - self.__t
    if dt < 0.005: return # Reject spuriously short pulses

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