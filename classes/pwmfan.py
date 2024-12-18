import os
import time
import json
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

logger = Logs().get_logger()

default_curve:List[Tuple[float, float]] = [
  (75.0, 100.0),  # Above 75°C, fan speed at 100%
  (70.0, 85.0),   # Above 70°C, fan speed at 85%
  (65.0, 70.0),   # Above 65°C, fan speed at 70%
  (60.0, 55.0),   # Above 60°C, fan speed at 55%
  (50.0, 45.0),   # Above 50°C, fan speed at 45%
  (40.0, 35.0),   # Above 40°C, fan speed at 35%
  (30.0, 30.0)    # Above 30°C, fan speed at 30%
]

def parse_duty_cycles(data:dict) -> List[Tuple[float, float]]:
  """
  Parse the duty cycles data from a given dictionary.

  This function now assumes that the input data is a dictionary where the keys are temperatures
  (as strings or numbers) and the values are corresponding fan speeds (as numbers or floats).
  The function converts each key-value pair into a tuple of floats (temperature, fan speed).

  Args:
    data (dict): A dictionary where each key is a temperature (int or float) and each value is the corresponding fan speed (int or float).

  Returns:
    list of tuple: A list of tuples, each containing two float values (temperature, fan speed), sorted by temperature.

  Raises:
    ValueError: If the temperature or speed values are not convertible to floats.

  Example:
    >>> data = {"70": 100.0, "65": 85.0, "60": 70.0, "55": 55.0, "45": 45.0, "35": 35.0, "30": 30.0}
    >>> parse_duty_cycles(data)
    [(30.0, 30.0), (35.0, 35.0), (45.0, 45.0), (55.0, 55.0), (60.0, 70.0), (65.0, 85.0), (70.0, 100.0)]
  """
  try:
    return [(float(temp), float(speed)) for temp, speed in data.items()]
  except ValueError as e:
    raise ValueError("One or more temperature or speed values are invalid. Could not convert to float.") from e


def load_fan_curve(fan_curve:str) -> List[Tuple[float, float]]:
  """
  Load and parse a fan curve file containing duty cycle data.

  This function attempts to read a JSON file specified by the `fan_curve` path, then parses
  the duty cycles from it. If there are issues during reading or parsing, detailed error messages 
  are logged and appropriate exceptions are raised.

  Args:
    fan_curve (str): The filename of the JSON file containing the fan curve data.

  Returns:
    list of tuple: A list of duty cycles (temperature, fan speed) parsed from the file.

  Raises:
    FileNotFoundError: If the specified file does not exist.
    PermissionError: If the program does not have permission to access the file.
    IOError: For any IO-related errors when attempting to open or read the file.
    ValueError: If the file contains invalid JSON or the duty cycles data is malformed.
    Exception: Any other unexpected errors during file handling or parsing.
  
  Example:
    >>> fan_curve_name = "fan_curve"
    >>> load_fan_curve(fan_curve_name)
    [(30.0, 1500.0), (40.0, 2000.0), (50.0, 2500.0)]
  """
  try:
    root_path = os.path.expanduser('~/fan_curves')
    json_filepath = os.path.join(root_path, f"{fan_curve}.json")
    logger.info(f'Loading custom fan curve file: {json_filepath}')
    with open(json_filepath) as file:
      try:
        return parse_duty_cycles(json.load(file))
      except json.JSONDecodeError as e:
        logger.critical(f"Failed to decode JSON in file '{fan_curve}': {e}")
        raise ValueError(f"Invalid JSON in file '{fan_curve}'") from e
      except Exception as e:
        logger.critical(f"Unexpected error while loading duty cycles from '{fan_curve}': {e}")
        raise
  except FileNotFoundError as e:
    logger.critical(f"File '{fan_curve}' not found: {e}")
    raise FileNotFoundError(f"Could not find the specified fan curve file '{fan_curve}'") from e
  except PermissionError as e:
    logger.critical(f"Permission denied to access file '{fan_curve}': {e}")
    raise PermissionError(f"Permission denied to read the file '{fan_curve}'") from e
  except IOError as e:
    logger.critical(f"IO error while opening file '{fan_curve}': {e}")
    raise IOError(f"Error while opening file '{fan_curve}'") from e
  except Exception as e:
    logger.critical(f"Unexpected error occurred: {e}")
    raise

class Pwmfan:
  """
  This class controls a PWM fan based on the temperature readings of the Raspberry Pi.
  The fan speed is adjusted according to predefined temperature thresholds and their corresponding duty cycles.
  """
  __fan = None
  __duty_cycles = default_curve
  __default_duty:float = 25.0
  __t:float = time.time()
  __pulse:int = 2
  __frequency:int = 25000
  
  rpm:int = 0
  
  def __init__(self, fan_pin:int, speed_pin:int, fan_curve:str = None) -> None:
    """
    Initialize the PWM fan controller.
    
    Args:
      fan_pin (int): The GPIO pin number controlling the fan's power (PWM signal).
      speed_pin (int): The GPIO pin number connected to the fan's tachometer (for RPM feedback).
      fan_curve (str): The name of the custom fan curve json file (i.e. test loads the file test.json)
    """
    logger.info(f'FAN_PIN:{fan_pin}, FAN_SPEED_PIN:{speed_pin}')
    if fan_curve:
      self.__duty_cycles:List[Tuple[float, float]] = load_fan_curve(fan_curve)

    try:
      GPIO.setup(speed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.add_event_detect(speed_pin, GPIO.FALLING, self.__fell)
    except Exception as e:
      logger.critical(f'Failed to configure PWM Tach pin: {e}')
      return
    
    try:
      GPIO.setup(fan_pin, GPIO.OUT)
      self.__fan = GPIO.PWM(fan_pin, self.__frequency)
      self.__fan.start(0)
    except Exception as e:
      logger.critical(f'Failed to configure PWM Control pin: {e}')
      return
    
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
    except Exception as e:
      logger.error(f'An unknown error accured: {e}')
      return

    reading_c:float = float(result.stdout.split('=')[1].split("'")[0])
    reading_f:float = round(((reading_c * 9) / 5) + 32, 1)
    
    if not self.__fan: return
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
    dt = time.time() - self.__t
    if dt < 0.005: return

    freq = 1 / dt
    self.rpm = round((freq / self.__pulse) * 60, 1)
    logger.debug(f'fell: {n}, freq: {freq}, rpm: {self.rpm}')
    self.__t:float = time.time()


if __name__ == "__main__":
  fan_pin = 12
  fan_tach = 24
  
  fan = Pwmfan(fan_pin, fan_tach)
  
  try:
    while True:
      fan.main()
      time.sleep(30)
  except KeyboardInterrupt:
    fan.cleanup()
    logger.debug('Keyboard interupt pressed')