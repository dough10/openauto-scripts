from pynput import keyboard
from pynput.keyboard import Key, Controller

keycontroller = Controller()

default_level = 10
pressed = default_level

def on_press(key):
    global pressed
    if key == keyboard.Key.f8 and pressed < 102:
        pressed += 1
    if key == keyboard.Key.f7 and pressed > 0:
        pressed -= 1
    
def on_release(key):
    if key == keyboard.Key.f12:
        resetVol()

def resetVol():
    global pressed
    global default_level
    while pressed > default_level:
        keycontroller.press(Key.f7)
        keycontroller.release(Key.f7)

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

