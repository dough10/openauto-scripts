#!/usr/bin/env python3

import os
import time
from dotenv import load_dotenv

from classes.logs import Logs
from classes.pwmfan import Pwmfan
from classes.remote import Remote
from classes.dashcam import Dashcam
from classes.ignition import Ignition
from classes.vol import Volume

logger = Logs().get_logger()

load_dotenv()

START_DELAY = int(os.getenv('START_DELAY', 3))
IGN_PIN = int(os.getenv('IGN_PIN', 17))
LATCH_PIN = int(os.getenv('LATCH_PIN', 4))
IGN_LOW_TIME = int(os.getenv('IGN_LOW_TIME', 3))
REMOTE_PIN = int(os.getenv('REMOTE_PIN', 25))
FAN_PIN = int(os.getenv('FAN_PIN', 12))
FAN_SPEED_PIN = int(os.getenv('FAN_SPEED_PIN', 24))
CUSTOM_CURVE = os.getenv('CUSTOM_CURVE', None)
REC_LOC = os.getenv('REC_LOC', '~/Videos')

def feature_is_enabled(feature:str) -> bool:
  env:str = os.getenv(feature, 'false')
  return env.lower() in ['true', '1', 't', 'y', 'yes']

def delay_start(count:int) -> None:
  while count > 0:
    logger.debug(f'Starting in: {count}')
    count -= 1
    time.sleep(1)

rem = Remote(REMOTE_PIN)
if feature_is_enabled('PWM'): 
  fan = Pwmfan(FAN_PIN, FAN_SPEED_PIN, CUSTOM_CURVE)
if feature_is_enabled('VOL'): 
  vol = Volume()
if feature_is_enabled('DASHCAM'): 
  cam = Dashcam(location=REC_LOC)

def shutdown() -> None:
  if 'vol' in globals():
    vol.stop_listener()
  if 'cam' in globals(): 
    cam.stop()
  rem.off()
  rem.cleanup()
  if 'fan' in globals(): 
    fan.cleanup()
  time.sleep(2)
    
ign = Ignition(IGN_PIN, LATCH_PIN, IGN_LOW_TIME, shutdown)

delay_start(START_DELAY)

rem.on()

while ign.running:
  try:
    ign.main()
    if 'fan' in globals(): 
      fan.main()
    time.sleep(1)
  except KeyboardInterrupt:
    break