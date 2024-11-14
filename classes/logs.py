import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# Fetch log level from the environment variable (default to 'WARNING')
log_level_str = os.getenv('LOG_LEVEL', 'WARNING').upper()

try:
  log_level = getattr(logging, log_level_str)
except AttributeError:
  raise ValueError(f"Invalid log level: {log_level_str}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")

class Logs:
  def __init__(self, filename: str, max_bytes: int = 5_000_000, backup_count: int = 5):
    filename = os.path.basename(filename)
    
    self.__logger = logging.getLogger('openauto-scripts')
    self.__logger.setLevel(log_level)

    if not self.__logger.hasHandlers():
      # Create a rotating file handler
      file_handler = RotatingFileHandler(f'{filename}.log', maxBytes=max_bytes, backupCount=backup_count)
      formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      file_handler.setFormatter(formatter)
      self.__logger.addHandler(file_handler)

      # Create a stream handler for console output
      stream_handler = logging.StreamHandler()
      stream_handler.setFormatter(formatter)
      self.__logger.addHandler(stream_handler)

      self.__logger.info(f"Log level set to: {log_level_str}")

  def get_logger(self):
    return self.__logger

# Example usage
if __name__ == "__main__":
  log = Logs(filename="example")
  logger = log.get_logger()
  logger.debug("This is a debug message")
  logger.info("This is an info message")
  logger.warning("This is a warning message")
