import os
import time
from dotenv import load_dotenv # type: ignore

from classes.pwmfan import Pwmfan
from classes.remote import Remote
from classes.dashcam import Dashcam
from classes.ignition import Ignition
from classes.vol import Volume

def feature_is_enabled(feature:str) -> bool:
  env:str = os.getenv(feature, 'false')
  return env.lower() in ['true', '1', 't', 'y', 'yes']

load_dotenv()

IGN_PIN = int(os.getenv('IGN_PIN', 17))
LATCH_PIN = int(os.getenv('LATCH_PIN', 4))
REMOTE_PIN = int(os.getenv('REMOTE_PIN', 25))
FAN_PIN = int(os.getenv('FAN_PIN', 12))
FAN_SPEED_PIN = int(os.getenv('FAN_SPEED_PIN', 24))
IGN_LOW_TIME = int(os.getenv('IGN_LOW_TIME', 3))
REC_LOC = os.getenv('REC_LOC', '~/Videos')

fan = Pwmfan(FAN_PIN, FAN_SPEED_PIN)
rem = Remote(REMOTE_PIN)
vol = Volume()
if feature_is_enabled('DASHCAM'): 
  cam = Dashcam(location=REC_LOC)

def shutdown() -> None:
  vol.stop_listener()
  rem.off()
  if cam: cam.stop()
  rem.cleanup()
  fan.cleanup()
    
ign = Ignition(IGN_PIN, LATCH_PIN, IGN_LOW_TIME, shutdown)

time.sleep(3)
rem.on()

while True:
  try:
    ign.main()
    fan.main()
    time.sleep(1)
  except KeyboardInterrupt:
    pass