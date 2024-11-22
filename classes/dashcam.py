import os
import time
import subprocess
from datetime import datetime

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs

logger = Logs().get_logger()

def wait(delay:int = 10):
  """
  Pauses the execution of the program for a given number of seconds, 
  printing the countdown each second.

  Args:
    delay (int): The number of seconds to wait. Default is 10 seconds.
  
  Example:
    wait(5)  # Waits for 5 seconds and prints the countdown.
  """
  while delay:
    print(f'{delay}')
    delay -= 1
    time.sleep(1)

class Dashcam:
  """
  Class for creating dashcam-style video recordings using Raspbian's built-in
  `raspivid` command. The recordings are saved in H264 format with filenames 
  based on the current date and time.
  
  Attributes:
    __file_path (str): The full path to the saved video file.
    __process (subprocess.Popen): The subprocess running the `raspivid` command.
  
  Methods:
    __init__(self, location: str, width: int, height: int, bitrate: float, fps: int):
        Initializes the dashcam and starts the video recording process.
    
    stop(self):
        Stops the video recording and saves the file.
  """
  def __init__(self, location:str = '/home/pi/Videos', width:int = 1280, height:int = 720, bitrate:float = 3.5, fps:int = 30) -> None:
    """
    Initializes the Dashcam object, starts video recording, and saves it to a timestamped file.
    
    Args:
      location (str): The directory where the video file will be saved. Default is '/home/pi/Videos'.
      width (int): The width (in pixels) of the video frame. Default is 1280.
      height (int): The height (in pixels) of the video frame. Default is 720.
      bitrate (float): The bitrate for video encoding in Mbps. Default is 3.5.
      fps (int): The frames per second for the video recording. Default is 30.
    
    Raises:
      Exception: If the specified location cannot be created or accessed.
    """
    if not os.path.exists(location):
      try:
        os.makedirs(location)
      except Exception as e:
        logger.critical('error creating file location: ', e)
        
    now = datetime.now()
    time_str = now.strftime("%m.%d.%Y.%H.%M")
    self.__file_path:str = f'{os.path.join(location, time_str)}.h264'

    logger.info(f'Starting {__file__}, path:{self.__file_path}')     
    self.__process = subprocess.Popen([
      "raspivid",
      "-n",
      "-h", str(height),
      "-w", str(width),
      "-b", str(bitrate * 1000000),
      "-fps", str(fps),
      "-t", "0",
      "-o", self.__file_path
    ])
        
  def stop(self) -> None:
    """
    Stops the video recording and saves the file.

    This method terminates the subprocess running `raspivid`, thus stopping the recording,
    and prints the location where the video has been saved.
    """
    logger.info(f'{self.__file_path} saved')
    self.__process.terminate()
 
if __name__ == "__main__":
  wait_time:int = 10

  cam = Dashcam()
  try:
    wait(wait_time)
    cam.stop()
  except KeyboardInterrupt:
    cam.stop()