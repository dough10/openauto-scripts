from pynput import keyboard
from pynput.keyboard import Controller, Listener


from classes.logs import Logs

  
keycontroller = Controller()
logger = Logs().get_logger()


class Volume:
  __default_level = 10
  __pressed = 10

  def __init__(self) -> None:
    logger.info(f'Starting {__file__}')
    with Listener(on_press=self.__on_press, on_release=self.__on_release) as monitor:
      monitor.join()

  def __on_release(self, key:str) -> None:
    if key == keyboard.Key.f12:
      self.__resetVol()

  def __on_press(self, key:str) -> None:
    if key == keyboard.Key.f8 and self.__pressed < 100:
      self.__pressed += 1
    if key == keyboard.Key.f7 and self.__pressed > 0:
      self.__pressed -= 1
    logger.debug(f'volume pressed: {self.__pressed}')

  def __resetVol(self) -> None:
    while self.__pressed > self.__default_level:
      keycontroller.press(keyboard.Key.f7)
      keycontroller.release(keyboard.Key.f7)
    while self.__pressed < self.__default_level:
      keycontroller.press(keyboard.Key.f8)
      keycontroller.release(keyboard.Key.f8)
    logger.info('volume reset')


if __name__ == "__main__":
  Volume()
