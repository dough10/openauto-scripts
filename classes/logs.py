import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler

log_level_str = os.getenv('LOG_LEVEL', 'WARNING').upper()

try:
  log_level = getattr(logging, log_level_str)
except AttributeError:
  raise ValueError(f"Invalid log level: {log_level_str}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.")

class Logs:
  def __init__(self, filename: str, max_bytes: int = 5_000_000, backup_count: int = 5):
    self.__logger = logging.getLogger('openauto-scripts')
    self.__logger.setLevel(level=log_level)

    if not self.__logger.handlers:
      file_handler = RotatingFileHandler(f'{os.path.basename(filename)}.log', maxBytes=max_bytes, backupCount=backup_count)
      formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
      file_handler.setFormatter(formatter)
      self.__logger.addHandler(file_handler)

      stream_handler = logging.StreamHandler()
      stream_handler.setFormatter(formatter)
      self.__logger.addHandler(stream_handler)

  def get_logger(self):
    return self.__logger
