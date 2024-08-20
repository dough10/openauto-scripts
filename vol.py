from pynput import keyboard
from pynput.keyboard import Key, Controller

keycontroller = Controller()

# Monitor times F12 is pressed
class Volume:
  __default_level = 10
  __pressed = 10

  def __init__(self):
    with keyboard.Listener(on_press=self.__on_press, on_release=self.__on_release) as listener:
      listener.join()

  def __on_release(self, key):
    if key == keyboard.Key.f12:
      self.__resetVol()

  def __on_press(self, key):
    if key == keyboard.Key.f8 and self.__pressed < 102:
      pressed += 1
    if key == keyboard.Key.f7 and self.__pressed > 0:
      pressed -= 1

  def __resetVol(self):
    print('volume reset')
    while self.__pressed > self.__default_level:
      keycontroller.press(Key.f7)
      keycontroller.release(Key.f7)

Volume()
