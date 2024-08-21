from classes.ignition import Ignition

IGN_PIN = 17
REMOTE_PIN = 25
FAN_PIN = 18

ignition = Ignition(IGN_PIN, REMOTE_PIN, FAN_PIN)

while True:
  ignition.main()
