from pynput.keyboard import Key, Controller, Listener

try:
  from classes.logs import Logs
except ModuleNotFoundError:
  from logs import Logs
  
keycontroller = Controller()
logger = Logs().get_logger()

class Volume:
  __default_level = 10
  __pressed = 10

  def __init__(self) -> None:
    logger.info('Starting vol.py')
    with Listener(on_press=self.__on_press, on_release=self.__on_release) as monitor:
      monitor.join()

  def __on_release(self, key:str) -> None:
    if key == Key.f12:
      logger.info('volume reset')
      self.__resetVol()

  def __on_press(self, key:str) -> None:
    if key == Key.f8 and self.__pressed < 102:
      pressed += 1
      logger.info('volume increased')
    if key == Key.f7 and self.__pressed > 0:
      pressed -= 1
      logger.info('volume decreased')

  def __resetVol(self) -> None:
    while self.__pressed > self.__default_level:
      keycontroller.press(Key.f7)
      keycontroller.release(Key.f7)