import threading
from pynput import keyboard
from pynput.keyboard import Controller, Listener

try:
  from classes.logs import Logs
  from classes.debounce import debounce
except ModuleNotFoundError:
  from debounce import debounce
  from logs import Logs
  
keycontroller = Controller()
logger = Logs().get_logger()


class Volume:
  """
  A class to monitor and control system volume using keyboard shortcuts.
  
  The class listens for specific keypress events (`F7`, `F8`, `F12`) to adjust and reset the 
  volume level. The volume level is simulated by sending key presses (`F7` to decrease volume 
  and `F8` to increase volume). It operates in a separate thread that listens for key events.
  
  Attributes:
    __default_level (int): The default volume level (set to 10).
    __pressed (int): The current volume level, initialized to 10.
    __listener_active (bool): A flag to control whether the listener should continue running.
  
  Methods:
    __init__(): Initializes the volume monitor and starts the listener in a separate thread.
    __start_listener(): Starts the keyboard listener and monitors keypress events.
    __on_press(key): Handles keypress events, adjusting the volume when `F7` or `F8` is pressed.
    __on_release(key): Handles key release events, resetting the volume when `F12` is pressed.
    __resetVol(): Resets the volume to the default level by simulating key presses.
    stop_listener(): Stops the listener thread and terminates volume monitoring.
  """
  __default_level = 10
  __pressed = 10
  __listener_active = True 

  def __init__(self) -> None:
    """
    Initializes the volume monitor, sets up the keyboard listener, and starts it in a separate thread.
    
    The listener listens for the `F7`, `F8`, and `F12` keys:
    - `F7` decreases the volume.
    - `F8` increases the volume.
    - `F12` resets the volume to the default level.
    
    Starts a background thread that listens for these keypress events.
    """
    logger.info(f'Starting volume monitor')
    listener_thread = threading.Thread(target=self.__start_listener)
    listener_thread.daemon = True
    listener_thread.start()

  def __start_listener(self):
    """
    Starts the keyboard listener to capture key events.

    The listener continuously monitors for keypress and key release events:
    - `on_press`: Calls `__on_press` method when a key is pressed.
    - `on_release`: Calls `__on_release` method when a key is released.

    The listener runs in a separate thread and waits for key events in a loop.
    """
    with Listener(on_press=self.__on_press, on_release=self.__on_release) as monitor:
      while self.__listener_active:
        monitor.join(timeout=1)  
    logger.info("Listener stopped.")

  def __on_press(self, key:str) -> None:
    """
    Handles the press of a key and adjusts the volume based on the key pressed.
    
    Specifically:
    - `F8` increases the volume level (up to 100).
    - `F7` decreases the volume level (down to 0).
    
    Args:
      key (str): The key that was pressed.
    """
    if key == keyboard.Key.f8 and self.__pressed < 100:
      self.__pressed += 1
      logger.debug(f'F8 pressed: {self.__pressed}')
    if key == keyboard.Key.f7 and self.__pressed > 0:
      self.__pressed -= 1
      logger.debug(f'F7 pressed: {self.__pressed}')

  def __on_release(self, key:str) -> None:
    """
    Handles the release of a key, performing an action when specific keys are released.
    
    Specifically:
    - `F12` resets the volume to the default level.
    
    Args:
      key (str): The key that was released.
    """
    if key == keyboard.Key.f12:
      self.__resetVol()
      
  @debounce(5)
  def __resetVol(self) -> None:
    """
    Resets the volume to the default level by simulating key presses (`F7`).
    
    This method decreases the volume by pressing `F7` until the volume reaches the default level.
    """
    while self.__pressed > self.__default_level:
      keycontroller.press(keyboard.Key.f7)
      keycontroller.release(keyboard.Key.f7)
    logger.info('volume reset')

  def stop_listener(self):
    """
    Stops the listener thread and disables the volume monitoring.
    
    Sets the `__listener_active` flag to False, which will stop the listener loop.
    """
    self.__listener_active = False
    logger.info("Stop listener request issued.")

if __name__ == "__main__":
  import time
  vol = Volume()
  time.sleep(10)
  vol.stop_listener() 