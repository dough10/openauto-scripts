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

logger = Logs().get_logger()

class Pwmfan:
  """
  This class controls a PWM fan based on the temperature readings of the Raspberry Pi.
  The fan speed is adjusted according to predefined temperature thresholds and their corresponding duty cycles.
  """
  # List of tuples defining temperature thresholds (°C) and corresponding fan speeds (duty cycle in percentage)
  __duty_cycles: List[Tuple[float, float]] = [
    (75.0, 100.0),  # Above 75°C, fan speed at 100%
    (70.0, 85.0),   # Above 70°C, fan speed at 85%
    (65.0, 70.0),   # Above 65°C, fan speed at 70%
    (60.0, 55.0),   # Above 60°C, fan speed at 55%
    (50.0, 45.0),   # Above 50°C, fan speed at 45%
    (40.0, 35.0),   # Above 40°C, fan speed at 35%
    (30.0, 30.0)    # Above 30°C, fan speed at 30%
  ]
  __default_duty:float = 25.0
  __t:float = time.time()
  __pulse:int = 2
  __frequency:int = 25000
  
  rpm:int = 0
  
  def __init__(self, fan_pin:int, speed_pin:int) -> None:
    """
    Initialize the PWM fan controller.
    
    Args:
      fan_pin (int): The GPIO pin number controlling the fan's power (PWM signal).
      speed_pin (int): The GPIO pin number connected to the fan's tachometer (for RPM feedback).
    """
    logger.info(f'Starting {__file__}, FAN_PIN:{fan_pin}, FAN_SPEED_PIN:{speed_pin}')
    GPIO.setup(speed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(speed_pin, GPIO.FALLING, self.__fell)
    GPIO.setup(fan_pin, GPIO.OUT)
    self.__fan = GPIO.PWM(fan_pin, self.__frequency)
    self.__fan.start(0)
    
  @debounce(30)
  def main(self) -> None:
    """
    Main control loop for adjusting the fan speed based on the temperature.
    
    This method reads the temperature from the Raspberry Pi and adjusts the PWM signal sent to
    the fan based on predefined thresholds and corresponding duty cycles.
    """
    try:
      result = subprocess.run(['/usr/bin/vcgencmd', 'measure_temp'], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
      logger.error(f"Error reading temperature: {e}")
      return

    reading_c:float = float(result.stdout.split('=')[1].split("'")[0])
    reading_f:float = round(((reading_c * 9) / 5) + 32, 1)
    
    for threshold, duty in self.__duty_cycles:
      if reading_c >= threshold:
        self.__fan.ChangeDutyCycle(duty)
        logger.debug(f"Fan speed ({self.rpm}rpm) adjusted to {duty}% for temperature {reading_c}°C ({reading_f}°F)")
        return

    self.__fan.ChangeDutyCycle(self.__default_duty)
    logger.debug(f"Fan speed ({self.rpm}rpm) set to {self.__default_duty}% (default) for temperature {reading_c}°C ({reading_f}°F)")

  def cleanup(self) -> None:
    """
    Clean up resources when the program ends.
    
    This includes stopping the PWM fan and cleaning up the GPIO settings.
    """
    self.__fan.stop()
    GPIO.cleanup()
    logger.info('stopping fan and cleaning up GPIO')

  def __fell(self, n:int) -> None:
    """
    This method is called whenever a falling edge is detected on the speed_pin (fan tachometer).
    
    It calculates the RPM of the fan based on the time between pulses.
    
    Args:
      n: The GPIO pin number (not used in this implementation).
    """
    logger.debug(f'fell: {n}')
    dt = time.time() - self.__t
    if dt < 0.005: return

    freq = 1 / dt
    self.rpm = round((freq / self.__pulse) * 60, 1)
    self.__t:float = time.time()


if __name__ == "__main__":
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  
  fan_pin = int(os.getenv('FAN_PIN', 12))
  fan_tach = int(os.getenv('FAN_SPEED_PIN', 24))
  
  fan = Pwmfan(fan_pin, fan_tach)
  
  try:
    while True:
      fan.main()
      time.sleep(30)
  except KeyboardInterrupt:
    fan.cleanup()
    logger.debug('Keyboard interupt pressed')