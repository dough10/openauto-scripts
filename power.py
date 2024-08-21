from classes.ignition import Ignition
from classes.pwmfan import Pwnfan

IGN_PIN = 17
REMOTE_PIN = 25
FAN_PIN = 18

ignition = Ignition(IGN_PIN, REMOTE_PIN)
fan = Pwnfan(FAN_PIN)

while True:
	fan.getCPUTemp()
	ignition.isRunning()
