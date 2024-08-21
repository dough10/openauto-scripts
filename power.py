from classes.ignition import Ignition
from classes.logs import Logs

IGN_PIN = 17
REMOTE_PIN = 25
FAN_PIN = 18

logger = Logs().get_logger()
ignition = Ignition(IGN_PIN, REMOTE_PIN, FAN_PIN)


def main():
  while True:
    ignition.main()

    
if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    logger.exception("main crashed. Error: %s", e) 
