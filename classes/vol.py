import os
import threading
from pynput import keyboard
from pynput.keyboard import Controller, Listener
from classes.logs import Logs
  
keycontroller = Controller()
logger = Logs().get_logger()


class Volume:
  __default_level = 10
  __pressed = 10
  __listener_active = True 

  def __init__(self) -> None:
    logger.info(f'Starting {os.path.basename(__file__)}')
    listener_thread = threading.Thread(target=self.__start_listener)
    listener_thread.daemon = True
    listener_thread.start()

  def __start_listener(self):
    with Listener(on_press=self.__on_press, on_release=self.__on_release) as monitor:
      while self.__listener_active:
        monitor.join(timeout=1)  
    logger.info("Listener stopped.")

  def __on_release(self, key:str) -> None:
    if key == keyboard.Key.f12:
      logger.debug('F12 keypress fired')
      self.__resetVol()

  def __on_press(self, key:str) -> None:
    if key == keyboard.Key.f8 and self.__pressed < 100:
      self.__pressed += 1
      logger.debug(f'F8 pressed: {self.__pressed}')
    if key == keyboard.Key.f7 and self.__pressed > 0:
      self.__pressed -= 1
      logger.debug(f'F7 pressed: {self.__pressed}')

  def __resetVol(self) -> None:
    while self.__pressed > self.__default_level:
      keycontroller.press(keyboard.Key.f7)
      keycontroller.release(keyboard.Key.f7)
    logger.info('volume reset')

  def stop_listener(self):
    self.__listener_active = False
    logger.info("Stop listener request issued.")

if __name__ == "__main__":
  vol = Volume()
  import time
  time.sleep(10)
  vol.stop_listener() 