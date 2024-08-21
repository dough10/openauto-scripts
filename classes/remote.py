import RPi.GPIO as GPIO


class Remote:
  def __init__(self, pin):
    self.__pin = pin
    GPIO.setup(self.__pin, GPIO.OUT)
    print('remote started')

  def on(self):
    GPIO.output(self.__pin, 1)
    print('Remote on')

  def off(self):
    GPIO.output(self.__pin, 0)
    print('remote off')
